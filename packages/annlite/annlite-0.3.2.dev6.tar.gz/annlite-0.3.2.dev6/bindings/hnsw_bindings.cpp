#include "hnswlib.h"
#include <assert.h>
#include <atomic>
#include <iostream>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdlib.h>
#include <thread>

namespace py = pybind11;
using namespace pybind11::literals; // needed to bring in _a literal

/*
 * replacement for the openmp '#pragma omp parallel for' directive
 * only handles a subset of functionality (no reductions etc)
 * Process ids from start (inclusive) to end (EXCLUSIVE)
 *
 * The method is borrowed from nmslib
 */
template <class Function>
inline void ParallelFor(size_t start, size_t end, size_t numThreads,
                        Function fn) {
  if (numThreads <= 0) {
    numThreads = std::thread::hardware_concurrency();
  }

  if (numThreads == 1) {
    for (size_t id = start; id < end; id++) {
      fn(id, 0);
    }
  } else {
    std::vector<std::thread> threads;
    std::atomic<size_t> current(start);

    // keep track of exceptions in threads
    // https://stackoverflow.com/a/32428427/1713196
    std::exception_ptr lastException = nullptr;
    std::mutex lastExceptMutex;

    for (size_t threadId = 0; threadId < numThreads; ++threadId) {
      threads.push_back(std::thread([&, threadId] {
        while (true) {
          size_t id = current.fetch_add(1);

          if ((id >= end)) {
            break;
          }

          try {
            fn(id, threadId);
          } catch (...) {
            std::unique_lock<std::mutex> lastExcepLock(lastExceptMutex);
            lastException = std::current_exception();
            /*
             * This will work even when current is the largest value that
             * size_t can fit, because fetch_add returns the previous value
             * before the increment (what will result in overflow
             * and produce 0 instead of current + 1).
             */
            current = end;
            break;
          }
        }
      }));
    }
    for (auto &thread : threads) {
      thread.join();
    }
    if (lastException) {
      std::rethrow_exception(lastException);
    }
  }
}

inline void assert_true(bool expr, const std::string &msg) {
  if (expr == false)
    throw std::runtime_error("Unpickle Error: " + msg);
  return;
}

template <typename dist_t, typename data_t = float> class Index {
public:
  Index(const std::string &space_name, const int dim)
      : space_name(space_name), dim(dim) {
    normalize = false;
    if (space_name == "l2") {
      l2space = new hnswlib::L2Space(dim);
    } else if (space_name == "ip") {
      l2space = new hnswlib::InnerProductSpace(dim);
    } else if (space_name == "cosine") {
      l2space = new hnswlib::InnerProductSpace(dim);
      normalize = true;
    } else {
      throw new std::runtime_error(
          "Space name must be one of l2, ip, or cosine.");
    }
    appr_alg = NULL;
    ep_added = true;
    index_inited = false;
    num_threads_default = std::thread::hardware_concurrency();

    default_ef = 10;
  }

  static const int ser_version = 1; // serialization version

  std::string space_name;
  int dim;
  size_t seed;
  size_t default_ef;

  bool index_inited;
  bool ep_added;
  bool normalize;
  int num_threads_default;
  hnswlib::labeltype cur_l;
  hnswlib::HierarchicalNSW<dist_t> *appr_alg;
  hnswlib::SpaceInterface<float> *l2space;

  ~Index() {
    delete l2space;
    if (appr_alg)
      delete appr_alg;
  }

  void init_new_index(const size_t maxElements, const size_t M,
                      const size_t efConstruction, const size_t random_seed) {
    if (appr_alg) {
      throw new std::runtime_error("The index is already initiated.");
    }
    cur_l = 0;
    appr_alg = new hnswlib::HierarchicalNSW<dist_t>(
        l2space, maxElements, M, efConstruction, random_seed);
    index_inited = true;
    ep_added = false;
    appr_alg->ef_ = default_ef;
    seed = random_seed;
  }

  void set_ef(size_t ef) {
    default_ef = ef;
    if (appr_alg)
      appr_alg->ef_ = ef;
  }

  void set_num_threads(int num_threads) {
    this->num_threads_default = num_threads;
  }

  void saveIndex(const std::string &path_to_index) {
    appr_alg->saveIndex(path_to_index);
  }

  void loadIndex(const std::string &path_to_index, size_t max_elements) {
    if (appr_alg) {
      std::cerr << "Warning: Calling load_index for an already inited index. "
                   "Old index is being deallocated.";
      delete appr_alg;
    }
    appr_alg = new hnswlib::HierarchicalNSW<dist_t>(l2space, path_to_index,
                                                    false, max_elements);
    cur_l = appr_alg->cur_element_count;
    index_inited = true;
  }

  void normalize_vector(float *data, float *norm_array) {
    float norm = 0.0f;
    for (int i = 0; i < dim; i++)
      norm += data[i] * data[i];
    norm = 1.0f / (sqrtf(norm) + 1e-30f);
    for (int i = 0; i < dim; i++)
      norm_array[i] = data[i] * norm;
  }

  void addItems(py::object input, py::object ids_ = py::none(),
                int num_threads = -1) {
    py::array_t<dist_t, py::array::c_style | py::array::forcecast> items(input);
    auto buffer = items.request();
    if (num_threads <= 0)
      num_threads = num_threads_default;

    size_t rows, features;

    if (buffer.ndim != 2 && buffer.ndim != 1)
      throw std::runtime_error("data must be a 1d/2d array");
    if (buffer.ndim == 2) {
      rows = buffer.shape[0];
      features = buffer.shape[1];
    } else {
      rows = 1;
      features = buffer.shape[0];
    }

    if (features != dim)
      throw std::runtime_error("wrong dimensionality of the vectors");

    // avoid using threads when the number of searches is small:
    if (rows <= num_threads * 4) {
      num_threads = 1;
    }

    std::vector<size_t> ids;

    if (!ids_.is_none()) {
      py::array_t<size_t, py::array::c_style | py::array::forcecast> items(
          ids_);
      auto ids_numpy = items.request();
      if (ids_numpy.ndim == 1 && ids_numpy.shape[0] == rows) {
        std::vector<size_t> ids1(ids_numpy.shape[0]);
        for (size_t i = 0; i < ids1.size(); i++) {
          ids1[i] = items.data()[i];
        }
        ids.swap(ids1);
      } else if (ids_numpy.ndim == 0 && rows == 1) {
        ids.push_back(*items.data());
      } else
        throw std::runtime_error("wrong dimensionality of the labels");
    }

    {

      int start = 0;
      if (!ep_added) {
        size_t id = ids.size() ? ids.at(0) : (cur_l);
        float *vector_data = (float *)items.data(0);
        std::vector<float> norm_array(dim);
        if (normalize) {
          normalize_vector(vector_data, norm_array.data());
          vector_data = norm_array.data();
        }
        appr_alg->addPoint((void *)vector_data, (size_t)id);
        start = 1;
        ep_added = true;
      }

      py::gil_scoped_release l;
      if (normalize == false) {
        ParallelFor(start, rows, num_threads, [&](size_t row, size_t threadId) {
          size_t id = ids.size() ? ids.at(row) : (cur_l + row);
          appr_alg->addPoint((void *)items.data(row), (size_t)id);
        });
      } else {
        std::vector<float> norm_array(num_threads * dim);
        ParallelFor(start, rows, num_threads, [&](size_t row, size_t threadId) {
          // normalize vector:
          size_t start_idx = threadId * dim;
          normalize_vector((float *)items.data(row),
                           (norm_array.data() + start_idx));

          size_t id = ids.size() ? ids.at(row) : (cur_l + row);
          appr_alg->addPoint((void *)(norm_array.data() + start_idx),
                             (size_t)id);
        });
      };
      cur_l += rows;
    }
  }

  std::vector<std::vector<data_t>>
  getDataReturnList(py::object ids_ = py::none()) {
    std::vector<size_t> ids;
    if (!ids_.is_none()) {
      py::array_t<size_t, py::array::c_style | py::array::forcecast> items(
          ids_);
      auto ids_numpy = items.request();
      std::vector<size_t> ids1(ids_numpy.shape[0]);
      for (size_t i = 0; i < ids1.size(); i++) {
        ids1[i] = items.data()[i];
      }
      ids.swap(ids1);
    }

    std::vector<std::vector<data_t>> data;
    for (auto id : ids) {
      data.push_back(appr_alg->template getDataByLabel<data_t>(id));
    }
    return data;
  }

  std::vector<hnswlib::labeltype> getIdsList() {

    std::vector<hnswlib::labeltype> ids;

    for (auto kv : appr_alg->label_lookup_) {
      ids.push_back(kv.first);
    }
    return ids;
  }

  py::dict getAnnData() const { /* WARNING: Index::getAnnData is not thread-safe
                                   with Index::addItems */

    std::unique_lock<std::mutex> templock(appr_alg->global);

    unsigned int level0_npy_size =
        appr_alg->cur_element_count * appr_alg->size_data_per_element_;
    unsigned int link_npy_size = 0;
    std::vector<unsigned int> link_npy_offsets(appr_alg->cur_element_count);

    for (size_t i = 0; i < appr_alg->cur_element_count; i++) {
      unsigned int linkListSize =
          appr_alg->element_levels_[i] > 0
              ? appr_alg->size_links_per_element_ * appr_alg->element_levels_[i]
              : 0;
      link_npy_offsets[i] = link_npy_size;
      if (linkListSize)
        link_npy_size += linkListSize;
    }

    char *data_level0_npy = (char *)malloc(level0_npy_size);
    char *link_list_npy = (char *)malloc(link_npy_size);
    int *element_levels_npy =
        (int *)malloc(appr_alg->element_levels_.size() * sizeof(int));

    hnswlib::labeltype *label_lookup_key_npy = (hnswlib::labeltype *)malloc(
        appr_alg->label_lookup_.size() * sizeof(hnswlib::labeltype));
    hnswlib::tableint *label_lookup_val_npy = (hnswlib::tableint *)malloc(
        appr_alg->label_lookup_.size() * sizeof(hnswlib::tableint));

    memset(label_lookup_key_npy, -1,
           appr_alg->label_lookup_.size() * sizeof(hnswlib::labeltype));
    memset(label_lookup_val_npy, -1,
           appr_alg->label_lookup_.size() * sizeof(hnswlib::tableint));

    size_t idx = 0;
    for (auto it = appr_alg->label_lookup_.begin();
         it != appr_alg->label_lookup_.end(); ++it) {
      label_lookup_key_npy[idx] = it->first;
      label_lookup_val_npy[idx] = it->second;
      idx++;
    }

    memset(link_list_npy, 0, link_npy_size);

    memcpy(data_level0_npy, appr_alg->data_level0_memory_, level0_npy_size);
    memcpy(element_levels_npy, appr_alg->element_levels_.data(),
           appr_alg->element_levels_.size() * sizeof(int));

    for (size_t i = 0; i < appr_alg->cur_element_count; i++) {
      unsigned int linkListSize =
          appr_alg->element_levels_[i] > 0
              ? appr_alg->size_links_per_element_ * appr_alg->element_levels_[i]
              : 0;
      if (linkListSize) {
        memcpy(link_list_npy + link_npy_offsets[i], appr_alg->linkLists_[i],
               linkListSize);
      }
    }

    py::capsule free_when_done_l0(data_level0_npy, [](void *f) { delete[] f; });
    py::capsule free_when_done_lvl(element_levels_npy,
                                   [](void *f) { delete[] f; });
    py::capsule free_when_done_lb(label_lookup_key_npy,
                                  [](void *f) { delete[] f; });
    py::capsule free_when_done_id(label_lookup_val_npy,
                                  [](void *f) { delete[] f; });
    py::capsule free_when_done_ll(link_list_npy, [](void *f) { delete[] f; });

    /*  TODO: serialize state of random generators appr_alg->level_generator_
     * and appr_alg->update_probability_generator_  */
    /*        for full reproducibility / to avoid re-initializing generators
     * inside Index::createFromParams         */

    return py::dict(
        "offset_level0"_a = appr_alg->offsetLevel0_,
        "max_elements"_a = appr_alg->max_elements_,
        "cur_element_count"_a = appr_alg->cur_element_count,
        "size_data_per_element"_a = appr_alg->size_data_per_element_,
        "label_offset"_a = appr_alg->label_offset_,
        "offset_data"_a = appr_alg->offsetData_,
        "max_level"_a = appr_alg->maxlevel_,
        "enterpoint_node"_a = appr_alg->enterpoint_node_,
        "max_M"_a = appr_alg->maxM_, "max_M0"_a = appr_alg->maxM0_,
        "M"_a = appr_alg->M_, "mult"_a = appr_alg->mult_,
        "ef_construction"_a = appr_alg->ef_construction_,
        "ef"_a = appr_alg->ef_, "has_deletions"_a = appr_alg->has_deletions_,
        "size_links_per_element"_a = appr_alg->size_links_per_element_,

        "label_lookup_external"_a = py::array_t<hnswlib::labeltype>(
            {appr_alg->label_lookup_.size()}, // shape
            {sizeof(
                hnswlib::labeltype)}, // C-style contiguous strides for double
            label_lookup_key_npy,     // the data pointer
            free_when_done_lb),

        "label_lookup_internal"_a = py::array_t<hnswlib::tableint>(
            {appr_alg->label_lookup_.size()}, // shape
            {sizeof(
                hnswlib::tableint)}, // C-style contiguous strides for double
            label_lookup_val_npy,    // the data pointer
            free_when_done_id),

        "element_levels"_a = py::array_t<int>(
            {appr_alg->element_levels_.size()}, // shape
            {sizeof(int)},      // C-style contiguous strides for double
            element_levels_npy, // the data pointer
            free_when_done_lvl),

        // linkLists_,element_levels_,data_level0_memory_
        "data_level0"_a = py::array_t<char>(
            {level0_npy_size}, // shape
            {sizeof(char)},    // C-style contiguous strides for double
            data_level0_npy,   // the data pointer
            free_when_done_l0),

        "link_lists"_a = py::array_t<char>(
            {link_npy_size}, // shape
            {sizeof(char)},  // C-style contiguous strides for double
            link_list_npy,   // the data pointer
            free_when_done_ll)

    );
  }

  py::dict getIndexParams() const { /* WARNING: Index::getAnnData is not
                                       thread-safe with Index::addItems */
    auto params = py::dict(
        "ser_version"_a =
            py::int_(Index<float>::ser_version), // serialization version
        "space"_a = space_name, "dim"_a = dim, "index_inited"_a = index_inited,
        "ep_added"_a = ep_added, "normalize"_a = normalize,
        "num_threads"_a = num_threads_default, "seed"_a = seed);

    if (index_inited == false)
      return py::dict(**params, "ef"_a = default_ef);

    auto ann_params = getAnnData();

    return py::dict(**params, **ann_params);
  }

  static Index<float> *createFromParams(const py::dict d) {

    // check serialization version
    assert_true(((int)py::int_(Index<float>::ser_version)) >=
                    d["ser_version"].cast<int>(),
                "Invalid serialization version!");

    auto space_name_ = d["space"].cast<std::string>();
    auto dim_ = d["dim"].cast<int>();
    auto index_inited_ = d["index_inited"].cast<bool>();

    Index<float> *new_index = new Index<float>(space_name_, dim_);

    /*  TODO: deserialize state of random generators into
     * new_index->level_generator_ and new_index->update_probability_generator_
     */
    /*        for full reproducibility / state of generators is serialized
     * inside Index::getIndexParams                      */
    new_index->seed = d["seed"].cast<size_t>();

    if (index_inited_) {
      new_index->appr_alg = new hnswlib::HierarchicalNSW<dist_t>(
          new_index->l2space, d["max_elements"].cast<size_t>(),
          d["M"].cast<size_t>(), d["ef_construction"].cast<size_t>(),
          new_index->seed);
      new_index->cur_l = d["cur_element_count"].cast<size_t>();
    }

    new_index->index_inited = index_inited_;
    new_index->ep_added = d["ep_added"].cast<bool>();
    new_index->num_threads_default = d["num_threads"].cast<int>();
    new_index->default_ef = d["ef"].cast<size_t>();

    if (index_inited_)
      new_index->setAnnData(d);

    return new_index;
  }

  static Index<float> *createFromIndex(const Index<float> &index) {
    return createFromParams(index.getIndexParams());
  }

  void setAnnData(const py::dict d) { /* WARNING: Index::setAnnData is not
                                         thread-safe with Index::addItems */

    std::unique_lock<std::mutex> templock(appr_alg->global);

    assert_true(appr_alg->offsetLevel0_ == d["offset_level0"].cast<size_t>(),
                "Invalid value of offsetLevel0_ ");
    assert_true(appr_alg->max_elements_ == d["max_elements"].cast<size_t>(),
                "Invalid value of max_elements_ ");

    appr_alg->cur_element_count = d["cur_element_count"].cast<size_t>();

    assert_true(appr_alg->size_data_per_element_ ==
                    d["size_data_per_element"].cast<size_t>(),
                "Invalid value of size_data_per_element_ ");
    assert_true(appr_alg->label_offset_ == d["label_offset"].cast<size_t>(),
                "Invalid value of label_offset_ ");
    assert_true(appr_alg->offsetData_ == d["offset_data"].cast<size_t>(),
                "Invalid value of offsetData_ ");

    appr_alg->maxlevel_ = d["max_level"].cast<int>();
    appr_alg->enterpoint_node_ = d["enterpoint_node"].cast<hnswlib::tableint>();

    assert_true(appr_alg->maxM_ == d["max_M"].cast<size_t>(),
                "Invalid value of maxM_ ");
    assert_true(appr_alg->maxM0_ == d["max_M0"].cast<size_t>(),
                "Invalid value of maxM0_ ");
    assert_true(appr_alg->M_ == d["M"].cast<size_t>(), "Invalid value of M_ ");
    assert_true(appr_alg->mult_ == d["mult"].cast<double>(),
                "Invalid value of mult_ ");
    assert_true(appr_alg->ef_construction_ ==
                    d["ef_construction"].cast<size_t>(),
                "Invalid value of ef_construction_ ");

    appr_alg->ef_ = d["ef"].cast<size_t>();
    appr_alg->has_deletions_ = d["has_deletions"].cast<bool>();

    assert_true(appr_alg->size_links_per_element_ ==
                    d["size_links_per_element"].cast<size_t>(),
                "Invalid value of size_links_per_element_ ");

    auto label_lookup_key_npy =
        d["label_lookup_external"]
            .cast<py::array_t<hnswlib::labeltype,
                              py::array::c_style | py::array::forcecast>>();
    auto label_lookup_val_npy =
        d["label_lookup_internal"]
            .cast<py::array_t<hnswlib::tableint,
                              py::array::c_style | py::array::forcecast>>();
    auto element_levels_npy =
        d["element_levels"]
            .cast<
                py::array_t<int, py::array::c_style | py::array::forcecast>>();
    auto data_level0_npy =
        d["data_level0"]
            .cast<
                py::array_t<char, py::array::c_style | py::array::forcecast>>();
    auto link_list_npy =
        d["link_lists"]
            .cast<
                py::array_t<char, py::array::c_style | py::array::forcecast>>();

    for (size_t i = 0; i < appr_alg->cur_element_count; i++) {
      if (label_lookup_val_npy.data()[i] < 0) {
        throw std::runtime_error("internal id cannot be negative!");
      } else {
        appr_alg->label_lookup_.insert(std::make_pair(
            label_lookup_key_npy.data()[i], label_lookup_val_npy.data()[i]));
      }
    }

    memcpy(appr_alg->element_levels_.data(), element_levels_npy.data(),
           element_levels_npy.nbytes());

    unsigned int link_npy_size = 0;
    std::vector<unsigned int> link_npy_offsets(appr_alg->cur_element_count);

    for (size_t i = 0; i < appr_alg->cur_element_count; i++) {
      unsigned int linkListSize =
          appr_alg->element_levels_[i] > 0
              ? appr_alg->size_links_per_element_ * appr_alg->element_levels_[i]
              : 0;
      link_npy_offsets[i] = link_npy_size;
      if (linkListSize)
        link_npy_size += linkListSize;
    }

    memcpy(appr_alg->data_level0_memory_, data_level0_npy.data(),
           data_level0_npy.nbytes());

    for (size_t i = 0; i < appr_alg->max_elements_; i++) {
      unsigned int linkListSize =
          appr_alg->element_levels_[i] > 0
              ? appr_alg->size_links_per_element_ * appr_alg->element_levels_[i]
              : 0;
      if (linkListSize == 0) {
        appr_alg->linkLists_[i] = nullptr;
      } else {
        appr_alg->linkLists_[i] = (char *)malloc(linkListSize);
        if (appr_alg->linkLists_[i] == nullptr)
          throw std::runtime_error(
              "Not enough memory: loadIndex failed to allocate linklist");

        memcpy(appr_alg->linkLists_[i],
               link_list_npy.data() + link_npy_offsets[i], linkListSize);
      }
    }
  }

  py::object knnQuery_return_numpy(py::object input, size_t k = 1,
                                   int num_threads = -1) {

    py::array_t<dist_t, py::array::c_style | py::array::forcecast> items(input);
    auto buffer = items.request();
    hnswlib::labeltype *data_numpy_l;
    dist_t *data_numpy_d;
    size_t rows, features;

    if (num_threads <= 0)
      num_threads = num_threads_default;

    {
      py::gil_scoped_release l;

      if (buffer.ndim != 2 && buffer.ndim != 1)
        throw std::runtime_error("data must be a 1d/2d array");
      if (buffer.ndim == 2) {
        rows = buffer.shape[0];
        features = buffer.shape[1];
      } else {
        rows = 1;
        features = buffer.shape[0];
      }

      // avoid using threads when the number of searches is small:

      if (rows <= num_threads * 4) {
        num_threads = 1;
      }

      data_numpy_l = new hnswlib::labeltype[rows * k];
      data_numpy_d = new dist_t[rows * k];

      if (normalize == false) {
        ParallelFor(0, rows, num_threads, [&](size_t row, size_t threadId) {
          std::priority_queue<std::pair<dist_t, hnswlib::labeltype>> result =
              appr_alg->searchKnn((void *)items.data(row), k);
          if (result.size() != k)
            throw std::runtime_error(
                "Cannot return the results in a contigious 2D array. Probably "
                "ef or M is too small");
          for (int i = k - 1; i >= 0; i--) {
            auto &result_tuple = result.top();
            data_numpy_d[row * k + i] = result_tuple.first;
            data_numpy_l[row * k + i] = result_tuple.second;
            result.pop();
          }
        });
      } else {
        std::vector<float> norm_array(num_threads * features);
        ParallelFor(0, rows, num_threads, [&](size_t row, size_t threadId) {
          size_t start_idx = threadId * dim;
          normalize_vector((float *)items.data(row),
                           (norm_array.data() + start_idx));

          std::priority_queue<std::pair<dist_t, hnswlib::labeltype>> result =
              appr_alg->searchKnn((void *)(norm_array.data() + start_idx), k);
          if (result.size() != k)
            throw std::runtime_error(
                "Cannot return the results in a contigious 2D array. Probably "
                "ef or M is too small");
          for (int i = k - 1; i >= 0; i--) {
            auto &result_tuple = result.top();
            data_numpy_d[row * k + i] = result_tuple.first;
            data_numpy_l[row * k + i] = result_tuple.second;
            result.pop();
          }
        });
      }
    }
    py::capsule free_when_done_l(data_numpy_l, [](void *f) { delete[] f; });
    py::capsule free_when_done_d(data_numpy_d, [](void *f) { delete[] f; });

    return py::make_tuple(
        py::array_t<hnswlib::labeltype>(
            {rows, k}, // shape
            {k * sizeof(hnswlib::labeltype),
             sizeof(
                 hnswlib::labeltype)}, // C-style contiguous strides for double
            data_numpy_l,              // the data pointer
            free_when_done_l),
        py::array_t<dist_t>(
            {rows, k}, // shape
            {k * sizeof(dist_t),
             sizeof(dist_t)}, // C-style contiguous strides for double
            data_numpy_d,     // the data pointer
            free_when_done_d));
  }

  py::object knnQuery_with_filter(py::object input,
                                  py::object candidate_ids_ = py::none(),
                                  size_t k = 1, int num_threads = -1) {

    py::array_t<dist_t, py::array::c_style | py::array::forcecast> items(input);
    auto buffer = items.request();
    hnswlib::labeltype *data_numpy_l;
    dist_t *data_numpy_d;

    if (num_threads <= 0)
      num_threads = num_threads_default;

    if (buffer.ndim != 2 && buffer.ndim != 1)
      throw std::runtime_error("data must be a 1d/2d array");

    size_t rows = 1;
    size_t features = buffer.shape[0];

    if (buffer.ndim == 2) {
      rows = buffer.shape[0];
      features = buffer.shape[1];
    }

    // avoid using threads when the number of searches is small:

    if (rows <= num_threads * 4) {
      num_threads = 1;
    }

    // FuseFilter constructing
    binary_fuse16_t filter(appr_alg->max_elements_);

    if (!candidate_ids_.is_none()) {
      py::array_t<size_t, py::array::c_style | py::array::forcecast> items(
          candidate_ids_);
      auto ids_numpy = items.request();

      if (ids_numpy.ndim == 1) {
        const size_t size = ids_numpy.shape[0];
        std::vector<uint64_t> big_set;
        big_set.reserve(size);
        for (size_t i = 0; i < size; i++) {
          big_set[i] = items.data()[i]; // we use contiguous values
        }

        if (!binary_fuse16_populate(big_set.data(), size, &filter)) {
          throw std::runtime_error("failure to populate the fuse filter");
        }
      } else
        throw std::runtime_error("wrong dimensionality of the filter labels");
    }

    {
      py::gil_scoped_release l;

      // would like to check the ownership of this data in more detail
      data_numpy_l = new hnswlib::labeltype[rows * k];
      data_numpy_d = new dist_t[rows * k];

      if (normalize == false) {
        ParallelFor(0, rows, num_threads, [&](size_t row, size_t threadId) {
          std::priority_queue<std::pair<dist_t, hnswlib::labeltype>> result =
              appr_alg->searchKnnWithFilter((void *)items.data(row), &filter,
                                            k);
          if (result.size() != k)
            throw std::runtime_error(
                "Cannot return the results in a contigious 2D array. Probably "
                "ef or M is too small");
          for (int i = k - 1; i >= 0; i--) {
            auto &result_tuple = result.top();
            data_numpy_d[row * k + i] = result_tuple.first;
            data_numpy_l[row * k + i] = result_tuple.second;
            result.pop();
          }
        });
      } else {
        std::vector<float> norm_array(num_threads * features);
        ParallelFor(0, rows, num_threads, [&](size_t row, size_t threadId) {
          float *data = (float *)items.data(row);

          size_t start_idx = threadId * dim;
          normalize_vector((float *)items.data(row),
                           (norm_array.data() + start_idx));

          std::priority_queue<std::pair<dist_t, hnswlib::labeltype>> result =
              appr_alg->searchKnnWithFilter(
                  (void *)(norm_array.data() + start_idx), &filter, k);
          if (result.size() != k)
            throw std::runtime_error(
                "Cannot return the results in a contigious 2D array. Probably "
                "ef or M is too small");
          for (int i = k - 1; i >= 0; i--) {
            auto &result_tuple = result.top();
            data_numpy_d[row * k + i] = result_tuple.first;
            data_numpy_l[row * k + i] = result_tuple.second;
            result.pop();
          }
        });
      }
    }

    py::capsule free_when_done_l(data_numpy_l, [](void *f) { delete[] f; });
    py::capsule free_when_done_d(data_numpy_d, [](void *f) { delete[] f; });

    return py::make_tuple(
        py::array_t<hnswlib::labeltype>(
            {rows, k}, // shape
            {k * sizeof(hnswlib::labeltype),
             sizeof(
                 hnswlib::labeltype)}, // C-style contiguous strides for double
            data_numpy_l,              // the data pointer
            free_when_done_l),
        py::array_t<dist_t>(
            {rows, k}, // shape
            {k * sizeof(dist_t),
             sizeof(dist_t)}, // C-style contiguous strides for double
            data_numpy_d,     // the data pointer
            free_when_done_d));
  }

  void markDeleted(size_t label) { appr_alg->markDelete(label); }

  void resizeIndex(size_t new_size) { appr_alg->resizeIndex(new_size); }

  size_t getMaxElements() const { return appr_alg->max_elements_; }

  size_t getCurrentCount() const { return appr_alg->cur_element_count; }
};

PYBIND11_PLUGIN(hnsw_bind) {
  py::module m("hnsw_bind");

  py::class_<Index<float>>(m, "Index")
      .def(py::init(&Index<float>::createFromParams), py::arg("params"))
      /* WARNING: Index::createFromIndex is not thread-safe with Index::addItems
       */
      .def(py::init(&Index<float>::createFromIndex), py::arg("index"))
      .def(py::init<const std::string &, const int>(), py::arg("space"),
           py::arg("dim"))
      .def("init_index", &Index<float>::init_new_index, py::arg("max_elements"),
           py::arg("M") = 16, py::arg("ef_construction") = 200,
           py::arg("random_seed") = 100)
      .def("knn_query", &Index<float>::knnQuery_return_numpy, py::arg("data"),
           py::arg("k") = 1, py::arg("num_threads") = -1)
      .def("knn_query_with_filter", &Index<float>::knnQuery_with_filter,
           py::arg("data"), py::arg("filters") = py::none(), py::arg("k") = 1,
           py::arg("num_threads") = -1)
      .def("add_items", &Index<float>::addItems, py::arg("data"),
           py::arg("ids") = py::none(), py::arg("num_threads") = -1)
      .def("get_items", &Index<float, float>::getDataReturnList,
           py::arg("ids") = py::none())
      .def("get_ids_list", &Index<float>::getIdsList)
      .def("set_ef", &Index<float>::set_ef, py::arg("ef"))
      .def("set_num_threads", &Index<float>::set_num_threads,
           py::arg("num_threads"))
      .def("save_index", &Index<float>::saveIndex, py::arg("path_to_index"))
      .def("load_index", &Index<float>::loadIndex, py::arg("path_to_index"),
           py::arg("max_elements") = 0)
      .def("mark_deleted", &Index<float>::markDeleted, py::arg("label"))
      .def("resize_index", &Index<float>::resizeIndex, py::arg("new_size"))
      .def("get_max_elements", &Index<float>::getMaxElements)
      .def("get_current_count", &Index<float>::getCurrentCount)
      .def_readonly("space", &Index<float>::space_name)
      .def_readonly("dim", &Index<float>::dim)
      .def_readwrite("num_threads", &Index<float>::num_threads_default)
      .def_property(
          "ef",
          [](const Index<float> &index) {
            return index.index_inited ? index.appr_alg->ef_ : index.default_ef;
          },
          [](Index<float> &index, const size_t ef_) {
            index.default_ef = ef_;
            if (index.appr_alg)
              index.appr_alg->ef_ = ef_;
          })
      .def_property_readonly("max_elements",
                             [](const Index<float> &index) {
                               return index.index_inited
                                          ? index.appr_alg->max_elements_
                                          : 0;
                             })
      .def_property_readonly("element_count",
                             [](const Index<float> &index) {
                               return index.index_inited
                                          ? index.appr_alg->cur_element_count
                                          : 0;
                             })
      .def_property_readonly("ef_construction",
                             [](const Index<float> &index) {
                               return index.index_inited
                                          ? index.appr_alg->ef_construction_
                                          : 0;
                             })
      .def_property_readonly("M",
                             [](const Index<float> &index) {
                               return index.index_inited ? index.appr_alg->M_
                                                         : 0;
                             })

      .def(py::pickle(
          [](const Index<float> &ind) { // __getstate__
            return py::make_tuple(
                ind.getIndexParams()); /* Return dict (wrapped in a tuple) that
                                          fully encodes state of the Index
                                          object */
          },
          [](py::tuple t) { // __setstate__
            if (t.size() != 1)
              throw std::runtime_error("Invalid state!");

            return Index<float>::createFromParams(t[0].cast<py::dict>());
          }))

      .def("__repr__", [](const Index<float> &a) {
        return "<pqlite.hnsw_bind.Index(space='" + a.space_name +
               "', dim=" + std::to_string(a.dim) + ")>";
      });

  return m.ptr();
}

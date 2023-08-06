/*
 * Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
 *
 * NVIDIA CORPORATION and its licensors retain all intellectual property
 * and proprietary rights in and to this software, related documentation
 * and any modifications thereto.  Any use, reproduction, disclosure or
 * distribution of this software and related documentation without an express
 * license agreement from NVIDIA CORPORATION is strictly prohibited.
 */


 /**
 * @file
 * @brief This file defines the types provided by the cuTensorNet library.
 */
#pragma once

#include <stdint.h>

#include <cuda_runtime.h>

/**
 * \brief The maximal length of the name for a user-provided mempool.
 */
#define CUTENSORNET_ALLOCATOR_NAME_LEN 64

/**
 * \brief cuTensorNet status type returns
 *
 * \details The type is used for function status returns. All cuTensorNet library functions return their status, which can have the following values.
 */
typedef enum
{
    /** The operation completed successfully.*/
    CUTENSORNET_STATUS_SUCCESS                = 0,
    /** The cuTensorNet library was not initialized.*/
    CUTENSORNET_STATUS_NOT_INITIALIZED        = 1,
    /** Resource allocation failed inside the cuTensorNet library.*/
    CUTENSORNET_STATUS_ALLOC_FAILED           = 3,
    /** An unsupported value or parameter was passed to the function (indicates a user error).*/
    CUTENSORNET_STATUS_INVALID_VALUE          = 7,
    /** The device is either not ready, or the target architecture is not supported.*/
    CUTENSORNET_STATUS_ARCH_MISMATCH          = 8,
    /** An access to GPU memory space failed, which is usually caused by a failure to bind a texture.*/
    CUTENSORNET_STATUS_MAPPING_ERROR          = 11,
    /** The GPU program failed to execute. This is often caused by a launch failure of the kernel on the GPU, which can be caused by multiple reasons.*/
    CUTENSORNET_STATUS_EXECUTION_FAILED       = 13,
    /** An internal cuTensorNet error has occurred.*/
    CUTENSORNET_STATUS_INTERNAL_ERROR         = 14,
    /** The requested operation is not supported.*/
    CUTENSORNET_STATUS_NOT_SUPPORTED          = 15,
    /** The functionality requested requires some license and an error was detected when trying to check the current licensing.*/
    CUTENSORNET_STATUS_LICENSE_ERROR          = 16,
    /** A call to CUBLAS did not succeed.*/
    CUTENSORNET_STATUS_CUBLAS_ERROR           = 17,
    /** Some unknown CUDA error has occurred.*/
    CUTENSORNET_STATUS_CUDA_ERROR             = 18,
    /** The provided workspace was insufficient.*/
    CUTENSORNET_STATUS_INSUFFICIENT_WORKSPACE = 19,
    /** The driver version is insufficient.*/
    CUTENSORNET_STATUS_INSUFFICIENT_DRIVER    = 20,
    /** An error occurred related to file I/O.*/
    CUTENSORNET_STATUS_IO_ERROR               = 21,
    /** The dynamically linked cuTENSOR library is incompatible.*/
    CUTENSORNET_STATUS_CUTENSOR_VERSION_MISMATCH = 22,
    /** Drawing device memory from a mempool is requested, but the mempool is not set.*/
    CUTENSORNET_STATUS_NO_DEVICE_ALLOCATOR    = 23,
    /** All hyper samples failed for one or more errors please enable LOGs via export CUTENSORNET_LOG_LEVEL= > 1 for details .*/
    CUTENSORNET_STATUS_ALL_HYPER_SAMPLES_FAILED    = 24,

} cutensornetStatus_t;

/**
 * \brief Encodes cuTensorNet's compute type (see "User Guide - Accuracy Guarantees" for details).
 */
typedef enum
{
    CUTENSORNET_COMPUTE_16F  = (1U<< 0U),  ///< floating-point: 5-bit exponent and 10-bit mantissa (aka half)
    CUTENSORNET_COMPUTE_16BF = (1U<< 10U),  ///< floating-point: 8-bit exponent and 7-bit mantissa (aka bfloat)
    CUTENSORNET_COMPUTE_TF32 = (1U<< 12U),  ///< floating-point: 8-bit exponent and 10-bit mantissa (aka tensor-float-32)
    CUTENSORNET_COMPUTE_32F  = (1U<< 2U),  ///< floating-point: 8-bit exponent and 23-bit mantissa (aka float)
    CUTENSORNET_COMPUTE_64F  = (1U<< 4U),  ///< floating-point: 11-bit exponent and 52-bit mantissa (aka double)
    CUTENSORNET_COMPUTE_8U   = (1U<< 6U),  ///< 8-bit unsigned integer
    CUTENSORNET_COMPUTE_8I   = (1U<< 8U),  ///< 8-bit signed integer
    CUTENSORNET_COMPUTE_32U  = (1U<< 7U),  ///< 32-bit unsigned integer
    CUTENSORNET_COMPUTE_32I  = (1U<< 9U),  ///< 32-bit signed integer
} cutensornetComputeType_t;

/**
 * \brief This enum lists graph algorithms that can be set.
 */
typedef enum
{
    CUTENSORNET_GRAPH_ALGO_RB,
    CUTENSORNET_GRAPH_ALGO_KWAY,
} cutensornetGraphAlgo_t;

/**
 * \brief This enum lists memory models used to determine workspace size
 */
typedef enum
{
    CUTENSORNET_MEMORY_MODEL_HEURISTIC,
    CUTENSORNET_MEMORY_MODEL_CUTENSOR,
} cutensornetMemoryModel_t;

/**
 * This enum lists all attributes of a ::cutensornetContractionOptimizerConfig_t that can be modified.
 */
typedef enum
{
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_NUM_PARTITIONS,          ///< int32_t: The network is recursively split over `num_partitions` until the size of each partition is less than or equal to the cutoff.
                                                                            ///<          The allowed range for `num_partitions` is [2, 30]. When the hyper-optimizer is disabled the default value is 8.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_CUTOFF_SIZE,             ///< int32_t: The network is recursively split over `num_partitions` until the size of each partition is less than or equal to this cutoff.
                                                                            ///<          The allowed range for `cutoff_size` is [4, 50]. When the hyper-optimizer is disabled the default value is 8.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_ALGORITHM,               ///< ::cutensornetGraphAlgo_t: the graph algorithm to be used in graph partitioning. Choices include
                                                                            ///<          CUTENSORNET_GRAPH_ALGO_KWAY (default) or CUTENSORNET_GRAPH_ALGO_RB.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_IMBALANCE_FACTOR,        ///< int32_t: Specifies the maximum allowed size imbalance among the partitions. Allowed range [30, 2000]. When the hyper-optimizer is disabled the default value is 200.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_NUM_ITERATIONS,          ///< int32_t: Specifies the number of iterations for the refinement algorithms at each stage of the uncoarsening process of the graph partitioner.
                                                                            ///<          Allowed range [1, 500]. When the hyper-optimizer is disabled the default value is 60.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_GRAPH_NUM_CUTS,                ///< int32_t: Specifies the number of different partitioning that the graph partitioner will compute. The final partitioning is the one that achieves the best edge-cut or communication volume.
                                                                            ///<          Allowed range [1, 40]. When the hyper-optimizer is disabled the default value is 10.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_RECONFIG_NUM_ITERATIONS,       ///< int32_t: Specifies the number of subtrees to be chosen for reconfiguration.
                                                                            ///<          A value of 0 disables reconfiguration. The default value is 500. The amount of time spent in reconfiguration, which usually dominates the pathfinder run time, is proportional to this.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_RECONFIG_NUM_LEAVES,           ///< int32_t: Specifies the maximum number of leaves in the subtree chosen for optimization in each reconfiguration iteration.
                                                                            ///<          The default value is 8. The default value is 500. The amount of time spent in reconfiguration, which usually dominates the pathfinder run time, is proportional to this.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SLICER_DISABLE_SLICING,        ///< int32_t: If set to 1, disables slicing regardless of memory available.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SLICER_MEMORY_MODEL,           ///< ::cutensornetMemoryModel_t: Memory model used to determine workspace size.
                                                                            ///<                           CUTENSORNET_MEMORY_MODEL_HEURISTIC uses a simple memory model that does not require external calls.
                                                                            ///<                           CUTENSORNET_MEMORY_MODEL_CUTENSOR (default) uses cuTENSOR to more precisely evaluate the amount of memory cuTENSOR will need for the contraction.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SLICER_MEMORY_FACTOR,          ///< int32_t: The memory limit for the first slice-finding iteration as a percentage of the workspace size.
                                                                            ///<          Allowed range [1, 100]. The default is 80 when using CUTENSORNET_MEMORY_MODEL_CUTENSOR for the memory model and 100 when using CUTENSORNET_MEMORY_MODEL_HEURISTIC.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SLICER_MIN_SLICES,             ///< int32_t: Minimum number of slices to produce at the first round of slicing. Default is 1.
    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SLICER_SLICE_FACTOR,           ///< int32_t: Factor by which to increase the total number of slice at each slicing round. Default is 2.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_HYPER_NUM_SAMPLES,             ///< int32_t: Number of hyper-optimizer random samples. Default 0 (disabled).

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SIMPLIFICATION_DISABLE_DR,     ///< int32_t: If set to 1, disable deferred rank simplification.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_SEED,                          ///< int32_t: Random seed to be used internally in order to reproduce same path.

    CUTENSORNET_CONTRACTION_OPTIMIZER_CONFIG_HYPER_NUM_THREADS,             ///< int32_t: Number of parallel hyper-optimizer threads. Default is number-of-cores / 2.
                                                                            ///<          When user-provided, it will be limited by the number of cores.

} cutensornetContractionOptimizerConfigAttributes_t;

/**
 * This enum lists all attributes of a ::cutensornetContractionOptimizerInfo_t that are accessible.
 */
typedef enum
{
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_NUM_SLICES,       ///< int64_t: Total number of slices.
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_NUM_SLICED_MODES, ///< int32_t: Total number of sliced modes.
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_SLICED_MODE,      ///< int32_t* slices: slices[i] with i < \p numSlices, corresponding to the i-th sliced mode name (see \p modesIn w.r.t. cutensornetCreateNetworkDescriptor()).
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_SLICED_EXTENT,    ///< int64_t* slices: slices[i] with i < \p numSlices, corresponding to the i-th sliced mode extent (see \p extentsIn w.r.t. cutensornetCreateNetworkDescriptor()).
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_PATH,             ///< ::cutensornetContractionPath_t: Pointer to the contraction path.
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_PHASE1_FLOP_COUNT,///< double: FLOP count for the given network after phase 1 of pathfinding (i.e., before slicing and reconfig).
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_FLOP_COUNT,       ///< double: FLOP count for the given network after slicing.
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_LARGEST_TENSOR,   ///< double: Size of the largest intermediate tensor in bytes.
    CUTENSORNET_CONTRACTION_OPTIMIZER_INFO_SLICING_OVERHEAD, ///< double: Overhead due to slicing.
} cutensornetContractionOptimizerInfoAttributes_t;


/**
 * This enum lists all attributes of a ::cutensornetContractionAutotunePreference_t that are accessible.
 */
typedef enum
{
    CUTENSORNET_CONTRACTION_AUTOTUNE_MAX_ITERATIONS,   ///< int32_t: Maximal number of auto-tune iterations for each pairwise contraction (default: 3).
} cutensornetContractionAutotunePreferenceAttributes_t;

/**
 * \brief Opaque structure holding cuTensorNet's network descriptor.
 */
typedef void* cutensornetNetworkDescriptor_t;

/**
 * \brief Opaque structure holding cuTensorNet's contraction plan.
 */
typedef void* cutensornetContractionPlan_t;

/**
 * \brief Opaque structure holding cuTensorNet's library context.
 * \details This handle holds the cuTensorNet library context (device properties, system information, etc.).
 * The handle must be initialized and destroyed with cutensornetCreate() and cutensornetDestroy() functions,
 * respectively.
 */
typedef void* cutensornetHandle_t;

/**
 * \brief Opaque structure that holds information about the user-provided workspace.
 */
typedef void* cutensornetWorkspaceDescriptor_t;

/**
 * \brief Workspace preference enumeration.
 */
typedef enum 
{ 
    CUTENSORNET_WORKSIZE_PREF_MIN = 0,         ///< At least one algorithm will be available for each contraction 
    CUTENSORNET_WORKSIZE_PREF_RECOMMENDED = 1, ///< The most suitable algorithm will be available for each contraction 
    CUTENSORNET_WORKSIZE_PREF_MAX = 2,         ///< All algorithms will be available for each contraction 
} cutensornetWorksizePref_t;

/**
 * \brief Memory space enumeration for workspace allocation.
 */
typedef enum
{
    CUTENSORNET_MEMSPACE_DEVICE = 0,       ///< Device memory space
} cutensornetMemspace_t;

/**
 * \brief A pair of int32_t values (typically referring to tensor IDs inside of the network).
 */
typedef struct __attribute__((aligned(4), packed))
{
    int32_t first;  ///< the first tensor
    int32_t second; ///< the second tensor
} cutensornetNodePair_t;

/**
 * \brief Holds information about the contraction path.
 *
 * The provided path is interchangeable with the path returned by <a href="https://numpy.org/doc/stable/reference/generated/numpy.einsum_path.html">numpy.einsum_path</a>.
 */
typedef struct
{
    int32_t numContractions; ///< total number of tensor contractions.
    cutensornetNodePair_t* data; ///< array of size \p numContractions. The tensors corresponding to `data[i].first` and `data[i].second` will be contracted.
} cutensornetContractionPath_t;

/**
 * \brief Opaque structure holding cuTensorNet's pathfinder config.
 */
typedef void* cutensornetContractionOptimizerConfig_t;

/**
 * \brief Opaque structure holding information about the optimized path and the slices (see ::cutensornetContractionOptimizerInfoAttributes_t).
 */
typedef void* cutensornetContractionOptimizerInfo_t;

/**
 * \brief Opaque structure information about the auto-tuning phase.
 */
typedef void* cutensornetContractionAutotunePreference_t;

/**
 * \brief The device memory handler structure holds information about the user-provided, \em stream-ordered device memory pool (mempool).
 */
typedef struct { 
  /**
   * A pointer to the user-owned mempool/context object.
   */
  void* ctx;
  /**
   * A function pointer to the user-provided routine for allocating device memory of \p size on \p stream.
   *
   * The allocated memory should be made accessible to the current device (or more
   * precisely, to the current CUDA context bound to the library handle).
   *
   * This interface supports any stream-ordered memory allocator \p ctx. Upon success,
   * the allocated memory can be immediately used on the given stream by any
   * operations enqueued/ordered on the same stream after this call.
   *
   * It is the caller’s responsibility to ensure a proper stream order is established.
   *
   * The allocated memory should be at least 256-byte aligned.
   *
   * \param[in] ctx A pointer to the user-owned mempool object.
   * \param[out] ptr On success, a pointer to the allocated buffer.
   * \param[in] size The amount of memory in bytes to be allocated.
   * \param[in] stream The CUDA stream on which the memory is allocated (and the stream order is established).
   * \return Error status of the invocation. Return 0 on success and any nonzero integer otherwise. This function must not throw if it is a C++ function.
   *
   */
  int (*device_alloc)(void* ctx, void** ptr, size_t size, cudaStream_t stream);
  /**
   * A function pointer to the user-provided routine for deallocating device memory of \p size on \p stream.
   * 
   * This interface supports any stream-ordered memory allocator. Upon success, any 
   * subsequent accesses (of the memory pointed to by the pointer \p ptr) ordered after 
   * this call are undefined behaviors.
   *
   * It is the caller’s responsibility to ensure a proper stream order is established.
   *
   * If the arguments \p ctx and \p size are not the same as those passed to \p device_alloc to 
   * allocate the memory pointed to by \p ptr, the behavior is undefined.
   * 
   * The argument \p stream need not be identical to the one used for allocating \p ptr, as
   * long as the stream order is correctly established. The behavior is undefined if
   * this assumption is not held.
   *
   * \param[in] ctx A pointer to the user-owned mempool object.
   * \param[in] ptr The pointer to the allocated buffer.
   * \param[in] size The size of the allocated memory.
   * \param[in] stream The CUDA stream on which the memory is deallocated (and the stream ordering is established).
   * \return Error status of the invocation. Return 0 on success and any nonzero integer otherwise. This function must not throw if it is a C++ function.
   */
  int (*device_free)(void* ctx, void* ptr, size_t size, cudaStream_t stream); 
  /**
   * The name of the provided mempool.
   */
  char name[CUTENSORNET_ALLOCATOR_NAME_LEN];
} cutensornetDeviceMemHandler_t;

/**
 * \typedef cutensornetLoggerCallback_t
 * \brief A callback function pointer type for logging APIs. Use cutensornetLoggerSetCallback() to set the callback function.
 * \param[in] logLevel the log level
 * \param[in] functionName the name of the API that logged this message
 * \param[in] message the log message
 */
typedef void (*cutensornetLoggerCallback_t)(
    int32_t logLevel,
    const char* functionName,
    const char* message
);

/**
 * \typedef cutensornetLoggerCallbackData_t
 * \brief A callback function pointer type for logging APIs. Use cutensornetLoggerSetCallbackData() to set the callback function and user data.
 * \param[in] logLevel the log level
 * \param[in] functionName the name of the API that logged this message
 * \param[in] message the log message
 * \param[in] userData user's data to be used by the callback
 */
typedef void (*cutensornetLoggerCallbackData_t)(
    int32_t logLevel,
    const char* functionName,
    const char* message,
    void* userData
);

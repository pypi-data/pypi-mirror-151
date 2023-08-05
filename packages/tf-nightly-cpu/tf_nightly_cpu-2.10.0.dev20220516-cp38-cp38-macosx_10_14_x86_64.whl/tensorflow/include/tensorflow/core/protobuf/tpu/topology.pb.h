// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/tpu/topology.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3009000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3009002 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[2]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto;
namespace tensorflow {
namespace tpu {
class TPUHardwareFeature;
class TPUHardwareFeatureDefaultTypeInternal;
extern TPUHardwareFeatureDefaultTypeInternal _TPUHardwareFeature_default_instance_;
class TopologyProto;
class TopologyProtoDefaultTypeInternal;
extern TopologyProtoDefaultTypeInternal _TopologyProto_default_instance_;
}  // namespace tpu
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::tpu::TPUHardwareFeature* Arena::CreateMaybeMessage<::tensorflow::tpu::TPUHardwareFeature>(Arena*);
template<> ::tensorflow::tpu::TopologyProto* Arena::CreateMaybeMessage<::tensorflow::tpu::TopologyProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {
namespace tpu {

enum TPUHardwareFeature_EmbeddingFeature : int {
  TPUHardwareFeature_EmbeddingFeature_UNSUPPORTED = 0,
  TPUHardwareFeature_EmbeddingFeature_V1 = 1,
  TPUHardwareFeature_EmbeddingFeature_V2 = 2,
  TPUHardwareFeature_EmbeddingFeature_TPUHardwareFeature_EmbeddingFeature_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<::PROTOBUF_NAMESPACE_ID::int32>::min(),
  TPUHardwareFeature_EmbeddingFeature_TPUHardwareFeature_EmbeddingFeature_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<::PROTOBUF_NAMESPACE_ID::int32>::max()
};
bool TPUHardwareFeature_EmbeddingFeature_IsValid(int value);
constexpr TPUHardwareFeature_EmbeddingFeature TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_MIN = TPUHardwareFeature_EmbeddingFeature_UNSUPPORTED;
constexpr TPUHardwareFeature_EmbeddingFeature TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_MAX = TPUHardwareFeature_EmbeddingFeature_V2;
constexpr int TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_ARRAYSIZE = TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* TPUHardwareFeature_EmbeddingFeature_descriptor();
template<typename T>
inline const std::string& TPUHardwareFeature_EmbeddingFeature_Name(T enum_t_value) {
  static_assert(::std::is_same<T, TPUHardwareFeature_EmbeddingFeature>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function TPUHardwareFeature_EmbeddingFeature_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    TPUHardwareFeature_EmbeddingFeature_descriptor(), enum_t_value);
}
inline bool TPUHardwareFeature_EmbeddingFeature_Parse(
    const std::string& name, TPUHardwareFeature_EmbeddingFeature* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<TPUHardwareFeature_EmbeddingFeature>(
    TPUHardwareFeature_EmbeddingFeature_descriptor(), name, value);
}
// ===================================================================

class TPUHardwareFeature :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.tpu.TPUHardwareFeature) */ {
 public:
  TPUHardwareFeature();
  virtual ~TPUHardwareFeature();

  TPUHardwareFeature(const TPUHardwareFeature& from);
  TPUHardwareFeature(TPUHardwareFeature&& from) noexcept
    : TPUHardwareFeature() {
    *this = ::std::move(from);
  }

  inline TPUHardwareFeature& operator=(const TPUHardwareFeature& from) {
    CopyFrom(from);
    return *this;
  }
  inline TPUHardwareFeature& operator=(TPUHardwareFeature&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const TPUHardwareFeature& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const TPUHardwareFeature* internal_default_instance() {
    return reinterpret_cast<const TPUHardwareFeature*>(
               &_TPUHardwareFeature_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(TPUHardwareFeature& a, TPUHardwareFeature& b) {
    a.Swap(&b);
  }
  inline void Swap(TPUHardwareFeature* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(TPUHardwareFeature* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline TPUHardwareFeature* New() const final {
    return CreateMaybeMessage<TPUHardwareFeature>(nullptr);
  }

  TPUHardwareFeature* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<TPUHardwareFeature>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const TPUHardwareFeature& from);
  void MergeFrom(const TPUHardwareFeature& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(TPUHardwareFeature* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.tpu.TPUHardwareFeature";
  }
  protected:
  explicit TPUHardwareFeature(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  typedef TPUHardwareFeature_EmbeddingFeature EmbeddingFeature;
  static constexpr EmbeddingFeature UNSUPPORTED =
    TPUHardwareFeature_EmbeddingFeature_UNSUPPORTED;
  static constexpr EmbeddingFeature V1 =
    TPUHardwareFeature_EmbeddingFeature_V1;
  static constexpr EmbeddingFeature V2 =
    TPUHardwareFeature_EmbeddingFeature_V2;
  static inline bool EmbeddingFeature_IsValid(int value) {
    return TPUHardwareFeature_EmbeddingFeature_IsValid(value);
  }
  static constexpr EmbeddingFeature EmbeddingFeature_MIN =
    TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_MIN;
  static constexpr EmbeddingFeature EmbeddingFeature_MAX =
    TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_MAX;
  static constexpr int EmbeddingFeature_ARRAYSIZE =
    TPUHardwareFeature_EmbeddingFeature_EmbeddingFeature_ARRAYSIZE;
  static inline const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor*
  EmbeddingFeature_descriptor() {
    return TPUHardwareFeature_EmbeddingFeature_descriptor();
  }
  template<typename T>
  static inline const std::string& EmbeddingFeature_Name(T enum_t_value) {
    static_assert(::std::is_same<T, EmbeddingFeature>::value ||
      ::std::is_integral<T>::value,
      "Incorrect type passed to function EmbeddingFeature_Name.");
    return TPUHardwareFeature_EmbeddingFeature_Name(enum_t_value);
  }
  static inline bool EmbeddingFeature_Parse(const std::string& name,
      EmbeddingFeature* value) {
    return TPUHardwareFeature_EmbeddingFeature_Parse(name, value);
  }

  // accessors -------------------------------------------------------

  enum : int {
    kEmbeddingFeatureFieldNumber = 1,
  };
  // .tensorflow.tpu.TPUHardwareFeature.EmbeddingFeature embedding_feature = 1;
  void clear_embedding_feature();
  ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature embedding_feature() const;
  void set_embedding_feature(::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature value);

  // @@protoc_insertion_point(class_scope:tensorflow.tpu.TPUHardwareFeature)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  int embedding_feature_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto;
};
// -------------------------------------------------------------------

class TopologyProto :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.tpu.TopologyProto) */ {
 public:
  TopologyProto();
  virtual ~TopologyProto();

  TopologyProto(const TopologyProto& from);
  TopologyProto(TopologyProto&& from) noexcept
    : TopologyProto() {
    *this = ::std::move(from);
  }

  inline TopologyProto& operator=(const TopologyProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline TopologyProto& operator=(TopologyProto&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const TopologyProto& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const TopologyProto* internal_default_instance() {
    return reinterpret_cast<const TopologyProto*>(
               &_TopologyProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(TopologyProto& a, TopologyProto& b) {
    a.Swap(&b);
  }
  inline void Swap(TopologyProto* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(TopologyProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline TopologyProto* New() const final {
    return CreateMaybeMessage<TopologyProto>(nullptr);
  }

  TopologyProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<TopologyProto>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const TopologyProto& from);
  void MergeFrom(const TopologyProto& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(TopologyProto* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.tpu.TopologyProto";
  }
  protected:
  explicit TopologyProto(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kMeshShapeFieldNumber = 1,
    kDeviceCoordinatesFieldNumber = 4,
    kTpuHardwareFeatureFieldNumber = 5,
    kNumTasksFieldNumber = 2,
    kNumTpuDevicesPerTaskFieldNumber = 3,
  };
  // repeated int32 mesh_shape = 1;
  int mesh_shape_size() const;
  void clear_mesh_shape();
  ::PROTOBUF_NAMESPACE_ID::int32 mesh_shape(int index) const;
  void set_mesh_shape(int index, ::PROTOBUF_NAMESPACE_ID::int32 value);
  void add_mesh_shape(::PROTOBUF_NAMESPACE_ID::int32 value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >&
      mesh_shape() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >*
      mutable_mesh_shape();

  // repeated int32 device_coordinates = 4;
  int device_coordinates_size() const;
  void clear_device_coordinates();
  ::PROTOBUF_NAMESPACE_ID::int32 device_coordinates(int index) const;
  void set_device_coordinates(int index, ::PROTOBUF_NAMESPACE_ID::int32 value);
  void add_device_coordinates(::PROTOBUF_NAMESPACE_ID::int32 value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >&
      device_coordinates() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >*
      mutable_device_coordinates();

  // .tensorflow.tpu.TPUHardwareFeature tpu_hardware_feature = 5;
  bool has_tpu_hardware_feature() const;
  void clear_tpu_hardware_feature();
  const ::tensorflow::tpu::TPUHardwareFeature& tpu_hardware_feature() const;
  ::tensorflow::tpu::TPUHardwareFeature* release_tpu_hardware_feature();
  ::tensorflow::tpu::TPUHardwareFeature* mutable_tpu_hardware_feature();
  void set_allocated_tpu_hardware_feature(::tensorflow::tpu::TPUHardwareFeature* tpu_hardware_feature);
  void unsafe_arena_set_allocated_tpu_hardware_feature(
      ::tensorflow::tpu::TPUHardwareFeature* tpu_hardware_feature);
  ::tensorflow::tpu::TPUHardwareFeature* unsafe_arena_release_tpu_hardware_feature();

  // int32 num_tasks = 2;
  void clear_num_tasks();
  ::PROTOBUF_NAMESPACE_ID::int32 num_tasks() const;
  void set_num_tasks(::PROTOBUF_NAMESPACE_ID::int32 value);

  // int32 num_tpu_devices_per_task = 3;
  void clear_num_tpu_devices_per_task();
  ::PROTOBUF_NAMESPACE_ID::int32 num_tpu_devices_per_task() const;
  void set_num_tpu_devices_per_task(::PROTOBUF_NAMESPACE_ID::int32 value);

  // @@protoc_insertion_point(class_scope:tensorflow.tpu.TopologyProto)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 > mesh_shape_;
  mutable std::atomic<int> _mesh_shape_cached_byte_size_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 > device_coordinates_;
  mutable std::atomic<int> _device_coordinates_cached_byte_size_;
  ::tensorflow::tpu::TPUHardwareFeature* tpu_hardware_feature_;
  ::PROTOBUF_NAMESPACE_ID::int32 num_tasks_;
  ::PROTOBUF_NAMESPACE_ID::int32 num_tpu_devices_per_task_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// TPUHardwareFeature

// .tensorflow.tpu.TPUHardwareFeature.EmbeddingFeature embedding_feature = 1;
inline void TPUHardwareFeature::clear_embedding_feature() {
  embedding_feature_ = 0;
}
inline ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature TPUHardwareFeature::embedding_feature() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TPUHardwareFeature.embedding_feature)
  return static_cast< ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature >(embedding_feature_);
}
inline void TPUHardwareFeature::set_embedding_feature(::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature value) {
  
  embedding_feature_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TPUHardwareFeature.embedding_feature)
}

// -------------------------------------------------------------------

// TopologyProto

// repeated int32 mesh_shape = 1;
inline int TopologyProto::mesh_shape_size() const {
  return mesh_shape_.size();
}
inline void TopologyProto::clear_mesh_shape() {
  mesh_shape_.Clear();
}
inline ::PROTOBUF_NAMESPACE_ID::int32 TopologyProto::mesh_shape(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TopologyProto.mesh_shape)
  return mesh_shape_.Get(index);
}
inline void TopologyProto::set_mesh_shape(int index, ::PROTOBUF_NAMESPACE_ID::int32 value) {
  mesh_shape_.Set(index, value);
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TopologyProto.mesh_shape)
}
inline void TopologyProto::add_mesh_shape(::PROTOBUF_NAMESPACE_ID::int32 value) {
  mesh_shape_.Add(value);
  // @@protoc_insertion_point(field_add:tensorflow.tpu.TopologyProto.mesh_shape)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >&
TopologyProto::mesh_shape() const {
  // @@protoc_insertion_point(field_list:tensorflow.tpu.TopologyProto.mesh_shape)
  return mesh_shape_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >*
TopologyProto::mutable_mesh_shape() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.tpu.TopologyProto.mesh_shape)
  return &mesh_shape_;
}

// int32 num_tasks = 2;
inline void TopologyProto::clear_num_tasks() {
  num_tasks_ = 0;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 TopologyProto::num_tasks() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TopologyProto.num_tasks)
  return num_tasks_;
}
inline void TopologyProto::set_num_tasks(::PROTOBUF_NAMESPACE_ID::int32 value) {
  
  num_tasks_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TopologyProto.num_tasks)
}

// int32 num_tpu_devices_per_task = 3;
inline void TopologyProto::clear_num_tpu_devices_per_task() {
  num_tpu_devices_per_task_ = 0;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 TopologyProto::num_tpu_devices_per_task() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TopologyProto.num_tpu_devices_per_task)
  return num_tpu_devices_per_task_;
}
inline void TopologyProto::set_num_tpu_devices_per_task(::PROTOBUF_NAMESPACE_ID::int32 value) {
  
  num_tpu_devices_per_task_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TopologyProto.num_tpu_devices_per_task)
}

// repeated int32 device_coordinates = 4;
inline int TopologyProto::device_coordinates_size() const {
  return device_coordinates_.size();
}
inline void TopologyProto::clear_device_coordinates() {
  device_coordinates_.Clear();
}
inline ::PROTOBUF_NAMESPACE_ID::int32 TopologyProto::device_coordinates(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TopologyProto.device_coordinates)
  return device_coordinates_.Get(index);
}
inline void TopologyProto::set_device_coordinates(int index, ::PROTOBUF_NAMESPACE_ID::int32 value) {
  device_coordinates_.Set(index, value);
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TopologyProto.device_coordinates)
}
inline void TopologyProto::add_device_coordinates(::PROTOBUF_NAMESPACE_ID::int32 value) {
  device_coordinates_.Add(value);
  // @@protoc_insertion_point(field_add:tensorflow.tpu.TopologyProto.device_coordinates)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >&
TopologyProto::device_coordinates() const {
  // @@protoc_insertion_point(field_list:tensorflow.tpu.TopologyProto.device_coordinates)
  return device_coordinates_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::int32 >*
TopologyProto::mutable_device_coordinates() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.tpu.TopologyProto.device_coordinates)
  return &device_coordinates_;
}

// .tensorflow.tpu.TPUHardwareFeature tpu_hardware_feature = 5;
inline bool TopologyProto::has_tpu_hardware_feature() const {
  return this != internal_default_instance() && tpu_hardware_feature_ != nullptr;
}
inline void TopologyProto::clear_tpu_hardware_feature() {
  if (GetArenaNoVirtual() == nullptr && tpu_hardware_feature_ != nullptr) {
    delete tpu_hardware_feature_;
  }
  tpu_hardware_feature_ = nullptr;
}
inline const ::tensorflow::tpu::TPUHardwareFeature& TopologyProto::tpu_hardware_feature() const {
  const ::tensorflow::tpu::TPUHardwareFeature* p = tpu_hardware_feature_;
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TopologyProto.tpu_hardware_feature)
  return p != nullptr ? *p : *reinterpret_cast<const ::tensorflow::tpu::TPUHardwareFeature*>(
      &::tensorflow::tpu::_TPUHardwareFeature_default_instance_);
}
inline ::tensorflow::tpu::TPUHardwareFeature* TopologyProto::release_tpu_hardware_feature() {
  // @@protoc_insertion_point(field_release:tensorflow.tpu.TopologyProto.tpu_hardware_feature)
  
  ::tensorflow::tpu::TPUHardwareFeature* temp = tpu_hardware_feature_;
  if (GetArenaNoVirtual() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
  tpu_hardware_feature_ = nullptr;
  return temp;
}
inline ::tensorflow::tpu::TPUHardwareFeature* TopologyProto::unsafe_arena_release_tpu_hardware_feature() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.tpu.TopologyProto.tpu_hardware_feature)
  
  ::tensorflow::tpu::TPUHardwareFeature* temp = tpu_hardware_feature_;
  tpu_hardware_feature_ = nullptr;
  return temp;
}
inline ::tensorflow::tpu::TPUHardwareFeature* TopologyProto::mutable_tpu_hardware_feature() {
  
  if (tpu_hardware_feature_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::tpu::TPUHardwareFeature>(GetArenaNoVirtual());
    tpu_hardware_feature_ = p;
  }
  // @@protoc_insertion_point(field_mutable:tensorflow.tpu.TopologyProto.tpu_hardware_feature)
  return tpu_hardware_feature_;
}
inline void TopologyProto::set_allocated_tpu_hardware_feature(::tensorflow::tpu::TPUHardwareFeature* tpu_hardware_feature) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete tpu_hardware_feature_;
  }
  if (tpu_hardware_feature) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      ::PROTOBUF_NAMESPACE_ID::Arena::GetArena(tpu_hardware_feature);
    if (message_arena != submessage_arena) {
      tpu_hardware_feature = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, tpu_hardware_feature, submessage_arena);
    }
    
  } else {
    
  }
  tpu_hardware_feature_ = tpu_hardware_feature;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.tpu.TopologyProto.tpu_hardware_feature)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tpu
}  // namespace tensorflow

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature>() {
  return ::tensorflow::tpu::TPUHardwareFeature_EmbeddingFeature_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ftpu_2ftopology_2eproto

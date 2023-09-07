

/*
WARNING: THIS FILE IS AUTO-GENERATED. DO NOT MODIFY.

This file was generated from MapScan_.idl using "rtiddsgen".
The rtiddsgen tool is part of the RTI Connext distribution.
For more information, type 'rtiddsgen -help' at a command shell
or consult the RTI Connext manual.
*/

#ifndef MapScan__1514206070_h
#define MapScan__1514206070_h

#ifndef NDDS_STANDALONE_TYPE
#ifndef ndds_cpp_h
#include "ndds/ndds_cpp.h"
#endif
#else
#include "ndds_standalone_type.h"
#endif

namespace ssafy_msgs {
    namespace msg {
        namespace dds_ {

            extern const char *MapScan_TYPENAME;

            struct MapScan_Seq;
            #ifndef NDDS_STANDALONE_TYPE
            class MapScan_TypeSupport;
            class MapScan_DataWriter;
            class MapScan_DataReader;
            #endif

            class MapScan_ 
            {
              public:
                typedef struct MapScan_Seq Seq;
                #ifndef NDDS_STANDALONE_TYPE
                typedef MapScan_TypeSupport TypeSupport;
                typedef MapScan_DataWriter DataWriter;
                typedef MapScan_DataReader DataReader;
                #endif

                DDS_Long   run_ ;

            };
            #if (defined(RTI_WIN32) || defined (RTI_WINCE)) && defined(NDDS_USER_DLL_EXPORT_ssafy_msgs)
            /* If the code is building on Windows, start exporting symbols.
            */
            #undef NDDSUSERDllExport
            #define NDDSUSERDllExport __declspec(dllexport)
            #endif

            NDDSUSERDllExport DDS_TypeCode* MapScan__get_typecode(void); /* Type code */

            DDS_SEQUENCE(MapScan_Seq, MapScan_);

            NDDSUSERDllExport
            RTIBool MapScan__initialize(
                MapScan_* self);

            NDDSUSERDllExport
            RTIBool MapScan__initialize_ex(
                MapScan_* self,RTIBool allocatePointers,RTIBool allocateMemory);

            NDDSUSERDllExport
            RTIBool MapScan__initialize_w_params(
                MapScan_* self,
                const struct DDS_TypeAllocationParams_t * allocParams);  

            NDDSUSERDllExport
            void MapScan__finalize(
                MapScan_* self);

            NDDSUSERDllExport
            void MapScan__finalize_ex(
                MapScan_* self,RTIBool deletePointers);

            NDDSUSERDllExport
            void MapScan__finalize_w_params(
                MapScan_* self,
                const struct DDS_TypeDeallocationParams_t * deallocParams);

            NDDSUSERDllExport
            void MapScan__finalize_optional_members(
                MapScan_* self, RTIBool deletePointers);  

            NDDSUSERDllExport
            RTIBool MapScan__copy(
                MapScan_* dst,
                const MapScan_* src);

            #if (defined(RTI_WIN32) || defined (RTI_WINCE)) && defined(NDDS_USER_DLL_EXPORT_ssafy_msgs)
            /* If the code is building on Windows, stop exporting symbols.
            */
            #undef NDDSUSERDllExport
            #define NDDSUSERDllExport
            #endif
        } /* namespace dds_  */
    } /* namespace msg  */
} /* namespace ssafy_msgs  */

#endif /* MapScan_ */


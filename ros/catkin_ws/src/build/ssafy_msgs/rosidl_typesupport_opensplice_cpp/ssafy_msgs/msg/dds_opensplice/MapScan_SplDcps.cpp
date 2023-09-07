#include "MapScan_SplDcps.h"
#include "ccpp_MapScan_.h"

#include <v_copyIn.h>
#include <v_topic.h>
#include <os_stdlib.h>
#include <string.h>
#include <os_report.h>

v_copyin_result
__ssafy_msgs_msg_dds__MapScan___copyIn(
    c_base base,
    const struct ::ssafy_msgs::msg::dds_::MapScan_ *from,
    struct _ssafy_msgs_msg_dds__MapScan_ *to)
{
    v_copyin_result result = V_COPYIN_RESULT_OK;
    (void) base;

    to->run_ = (c_long)from->run_;
    return result;
}

void
__ssafy_msgs_msg_dds__MapScan___copyOut(
    const void *_from,
    void *_to)
{
    const struct _ssafy_msgs_msg_dds__MapScan_ *from = (const struct _ssafy_msgs_msg_dds__MapScan_ *)_from;
    struct ::ssafy_msgs::msg::dds_::MapScan_ *to = (struct ::ssafy_msgs::msg::dds_::MapScan_ *)_to;
    to->run_ = (::DDS::Long)from->run_;
}


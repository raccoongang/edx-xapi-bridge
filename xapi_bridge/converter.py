"""Convert tracking log entries to xAPI statements."""

from xapi_bridge import exceptions, settings
from xapi_bridge.statements import base, course, problem, video


TRACKING_EVENTS_TO_XAPI_STATEMENT_MAP = {

    # course enrollment
    'edx.course.enrollment.activated': course.CourseEnrollmentStatement,
    'edx.course.enrollment.deactivated': course.CourseUnenrollmentStatement,

    # course completion
    'edx.certificate.created': course.CourseCompletionStatement,

    # problems
    'problem_check': problem.ProblemCheckStatement,
    # 'problem_graded': problem.ProblemGradedStatement, # not interesting I think
    # 'problem_reset': problem.ProblemResetStatement,

    # video
    'ready_video': video.VideoStatement,
    'load_video': video.VideoStatement,
    'edx.video.loaded': video.VideoStatement,

    'play_video': video.VideoPlayStatement,
    'edx.video.played': video.VideoPlayStatement,

    'pause_video': video.VideoPauseStatement,
    'edx.video.paused': video.VideoPauseStatement,

    'stop_video': video.VideoCompleteStatement,
    'edx.video.stopped': video.VideoCompleteStatement,

    'seek_video': video.VideoSeekStatement,
    'edx.video.position.changed': video.VideoSeekStatement,

    'show_transcript': video.VideoTranscriptStatement,
    'hide_transcript': video.VideoTranscriptStatement,
    'edx.video.transcript.shown': video.VideoTranscriptStatement,
    'edx.video.transcript.hidden': video.VideoTranscriptStatement,
    'edx.video.closed_captions.shown': video.VideoTranscriptStatement,
    'edx.video.closed_captions.hidden': video.VideoTranscriptStatement,
}


def to_xapi(evt):
    """Return tuple of xAPI statements or None if ignored or unhandled event type."""

    # strip Video XBlock prefixes for checking
    event_type = evt['event_type'].replace("xblock-video.", "")

    if event_type in settings.IGNORED_EVENT_TYPES:
        return

    try:
        statement_class = TRACKING_EVENTS_TO_XAPI_STATEMENT_MAP[event_type]
    except KeyError:
        return

    try:
        statement = statement_class(evt)
        if hasattr(statement, 'version'):  # make sure it's a proper statement
            return (statement, )
        else:
            raise exceptions.XAPIMalformedStatementError
    except exceptions.XAPIMalformedStatementError:
        print "Skipping bad Statement {}".format(statement.to_json())
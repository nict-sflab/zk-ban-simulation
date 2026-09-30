PLATFORM = "twitch"
VERSION = "light"

ANALYSIS_OUTPUT_FILE = "result.csv"

ZIP_FOLDER = "./dsa_data"
CSV_FOLDER = "./dsa_data_csv"

ANALYSIS_START = "2025-07-31"
ANALYSIS_END = "2026-07-31"

PERIOD_UNIT = 1

ENCODING = "utf-8-sig"
BATCH_SIZE = 20000

DB_FILE = f"./{PLATFORM}.sqlite"
FILE_NAME = f"sor-{PLATFORM}-{{}}-light"

CSV_NAME_TEMPLATE =  f"{FILE_NAME}"
ZIP_NAME_FORMAT = f"{FILE_NAME}.zip"


# Date when the moderated content was originally created or posted.
AUTH_COL = "content_date"

# Date when the moderation action or revocation decision was applied.
REVOKE_COL = "application_date"

# Unique identifier of the SOR record.
ID_COL = "uuid"


# Decision about visibility of the content, such as removal or disabling.
VISIBILITY_COL = "decision_visibility"

# Decision about the user account, such as suspension or termination.
ACCOUNT_COL = "decision_account"

# Decision about the provision of the service, such as partial suspension.
PROVISION_COL = "decision_provision"

# Monetary decision, such as demonetization. This parser keeps it excluded.
MONETARY_COL = "decision_monetary"


# Type of content affected by the decision, such as text, image, video, or other.
CONTENT_TYPE_COL = "content_type"

# Free-text content type used when content_type is "other".
CONTENT_TYPE_OTHER_COL = "content_type_other"


# Decision columns that are collected but not used to build decision_text.
EXCLUDE_DECISION_COLS = (
)


# Columns describing the alleged violation or legal/policy basis.
VIOLATION_COLS = (
    "category",
    "category_specification",
    "illegal_content_legal_ground",
    "illegal_content_explanation",
    "incompatible_content_ground",
    "incompatible_content_explanation",
)


# Visibility decisions that mean the content itself was removed or disabled.
CONTENT_REVOCATION_DECISIONS = {
    "DECISION_VISIBILITY_CONTENT_REMOVED",
    "DECISION_VISIBILITY_CONTENT_DISABLED",
}


# Provision decisions that mean service provision was partially stopped.
ACCOUNT_STOP_PROVISION_DECISIONS = {
    "DECISION_PROVISION_PARTIAL_SUSPENSION",
}


# Keywords that indicate an account-level enforcement action.
ACCOUNT_ACTION_KEYWORDS = (
    "ACCOUNT_SUSPEND",
    "ACCOUNT_SUSPENDED",
    "ACCOUNT_SUSPENSION",
    "ACCOUNT_TERMINATE",
    "ACCOUNT_TERMINATED",
    "ACCOUNT_TERMINATION",
    "ACCOUNT_DISABLE",
    "ACCOUNT_DISABLED",
    "ACCOUNT_DEACTIVATE",
    "ACCOUNT_DEACTIVATED",
    "ACCOUNT_DELETE",
    "ACCOUNT_DELETED",
    "ACCOUNT_REMOVE",
    "ACCOUNT_REMOVED",
    "ACCOUNT_BLOCK",
    "ACCOUNT_BLOCKED",
)


# Values treated as empty or missing in SOR fields.
NULL_LIKE = {"", "[]", "null", "none", "nan", "na", "n/a", "undefined"}

VIOLATION_COLS = (
    "category",
    "category_specification",
    "illegal_content_legal_ground",
    "illegal_content_explanation",
    "incompatible_content_ground",
    "incompatible_content_explanation",
)

CONTENT_REVOCATION_DECISIONS = {
    "DECISION_VISIBILITY_CONTENT_REMOVED",
    "DECISION_VISIBILITY_CONTENT_DISABLED",
}

ACCOUNT_STOP_PROVISION_DECISIONS = {
    "DECISION_PROVISION_PARTIAL_SUSPENSION",
}

GOOD_CONTENT_KEYWORDS = (
    "TEXT",
    "POST",
    "COMMENT",
    "REPLY",
    "SUBMISSION",
    "VIDEO",
    "IMAGE",
    "PHOTO",
    "AUDIO",
    "LINK",
    "MESSAGE",
    "CHAT",
    "PRIVATE_MESSAGE",
    "DIRECT_MESSAGE",
    "DM",
)

BAD_CONTENT_KEYWORDS = (
    "OTHER",
    "ACCOUNT",
    "PROFILE",
    "USER",
    "SERVICE",
    "PROVISION",
    "CHANNEL",
    "COMMUNITY",
    "GROUP",
    "PAGE",
    "SHOP",
    "PRODUCT",
    "AD",
    "ADS",
    "ADVERTISEMENT",
    "MONETARY",
    "PAYMENT",
)

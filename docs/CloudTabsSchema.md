# Safari Cloud Tabs

Safari stores cloud tab data in a sqlite3 db file: `CloudTabs.db`, located at `~/Library/Containers/com.apple.Safari/Data/Library/Safari/CloudTabs.db`


## cloud_tabs

This table contains each open tab stored in iCloud.
Notably the `device_uuid` field is a foreign key relationship to the
`cloud_tab_devices` table, which stores the name of each device Safari has
registered with iCloud.

| Field | Type |
|-------|------|
| tab_uuid | TEXT |
| system_fields | BLOB |
| device_uuid | TEXT |
| position | BLOB |
| title | TEXT |
| url | TEXT |
| is_showing_reader | BOOLEAN |
| is_pinned | BOOLEAN |
| reader_scroll_position_page_index | INTEGER |
| scene_id | TEXT |

## cloud_tab_devices

This table stores devices registered by Safari in iCloud. For the most part
this is useful to join onto the `cloud_tabs` table to obtain device names.

| Field | Type |
|-------|------|
| device_uuid | TEXT |
| system_fields | BLOB |
| device_name | TEXT |
| has_duplicate_device_name | BOOLEAN |
| is_ephemeral_device | BOOLEAN |
| last_modified | REAL |
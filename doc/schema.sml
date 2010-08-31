# Stupid Markup Language.  See sml.js (which is included elsewhere...) for 
# the gory details.  It's really simple.

# DB schema at HEAD revision.
# Keep this file up-to-date with any server code changes!

event
    :string where
        Human-friendly description of event location
    :timestamp when
        Time the event starts
    :string desc
        Event description
    :bool broadcast
        If true, visible to all users; if false, visible only to friends
    :latlng posted_from
        Location of event creator when event was created
    :latlng location
        Coordinates of event
    :string category
        Optional event category
    :string creator
        Username of event creator
    :timestamp created
        Time of event creation
    :uuid revision
        Event revision; see event management API docs
        
attendance
    :oid event
        Event id
    :string username
        Username of attendee
    :timestamp timestamp
        Time of last attendance status change for the attendee
    :int status
        Attendance status; see API docs for possible values
        
comment
    :string nonce
        Nonce value to prevent comment dupes
    :string comment
        Comment body
    :timestamp timestamp
        Time comment was posted
    :oid event
        Event comment is attached to
    :username user
        Comment creator
        
session
    :timestamp timestamp
        Timestamp of session creation
    :string username
        Username of session owner
        
user
    :string username
        User's username
    :string password
        Hashed and salted password
    :uuid revision
        User revision; see API docs for details
    :timestamp created
        Timestamp of user creation
        
friend
    :string from
        Username of first friend in relationship
    :string to
        Username of second friend in relationship
    :int status
        Status of friendship; see API docs for details
        
notification_reg
    :string user
        Username for which the notifications are registered
    :string client_type
        Client type registered for notifications
    :string client_id
        Unique client identifier
    :opaque client_extra
        Opaque client data used by client-type specific notifier

# In the future we'll be able to have a fancy little javascript display
# for this file.  In the meantime, it's pretty human parsable.
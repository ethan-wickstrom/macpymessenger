on checkCompatibility(phoneNumber)
    tell application "Messages"
        -- Ensure the Messages app is running
        if not running then
            launch
            delay 1 -- Wait for the application to fully launch
        end if

        -- Start a new conversation or get an existing one
        set targetService to first service whose service type = iMessage
        set targetBuddy to participant phoneNumber of targetService

        -- Check if the recipient is iMessage compatible
        if targetBuddy exists then
            return true
        else
            return false
        end if
    end tell
end checkCompatibility


on run argv
    set phoneNumber to item 1 of argv

    if checkCompatibility(phoneNumber) then
        return true
    else
        return false
    end if
end run
on sendMessage(phoneNumber, messageText)
    tell application "Messages"
        if not running then
            launch
            delay 1 -- Wait for the application to fully launch
        end if

        set targetService to first service whose service type = iMessage
        set targetBuddy to buddy phoneNumber of targetService

        -- Attempt to send the message
        try
            send messageText to targetBuddy
            return "Success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
end sendMessage


on run argv
    set phoneNumber to item 1 of argv
    set messageText to item 2 of argv

    set result to sendMessage(phoneNumber, messageText)
    return result
end run
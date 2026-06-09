on sendMessage(phoneNumber, messageText)
    tell application "Messages"
        if not running then
            launch
            delay 1 -- Wait for the application to fully launch
        end if

        set targetService to first service whose service type = iMessage
        set targetBuddy to buddy phoneNumber of targetService

        -- Let delivery errors propagate so osascript exits non-zero
        send messageText to targetBuddy
    end tell
end sendMessage


on run argv
    set phoneNumber to item 1 of argv
    set messageText to item 2 of argv

    set delaySeconds to 0
    if (count of argv) >= 3 then
        set delaySeconds to (item 3 of argv) as integer
    end if
    if delaySeconds > 0 then delay delaySeconds

    sendMessage(phoneNumber, messageText)
    return "Success"
end run

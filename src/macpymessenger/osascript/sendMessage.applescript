use framework "Foundation"
use scripting additions

on decodeBase64(encodedText)
    set decodedData to current application's NSData's alloc()'s initWithBase64EncodedString:encodedText options:0
    if decodedData is missing value then error "Invalid encoded text."

    set decodedText to current application's NSString's alloc()'s initWithData:decodedData encoding:(current application's NSUTF8StringEncoding)
    if decodedText is missing value then error "Invalid UTF-8 text."

    return decodedText as text
end decodeBase64

on sendMessage(recipient, messageBody, delaySeconds)
    if delaySeconds > 0 then delay delaySeconds

    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy recipient of targetService
        send messageBody to targetBuddy
    end tell
end sendMessage

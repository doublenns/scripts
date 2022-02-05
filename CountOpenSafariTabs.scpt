#!/usr/bin/env osascript
-- Original Author: Chad Armstrong
-- Source: https://gist.github.com/edenwaith/2213a764ccb091d6a03989f238efb63f

-- Description: Count the number of open windows and tabs in Safari

tell application "Safari"

    --Variables
    set windowCount to count of windows
    set windowList to every window
    set totalTabCount to 0

    -- Loop through each window to count the number of open tabs
    repeat with win in windowList
        try
            set tabcount to number of tabs in win
            set totalTabCount to totalTabCount + tabcount
            -- log "tab count: " & tabcount & " totalTabCount: " & totalTabCount
        on error errmsg
            -- Often getting error message like this:
            -- "Safari got an error: AppleEvent handler failed."
            -- log "error message: " & errmsg
        end try
    end repeat

    log "There are " & windowCount & " Safari windows open."
    log "There are " & totalTabCount & " Safari tabs open."

end tell
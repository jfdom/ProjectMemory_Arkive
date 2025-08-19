// Supervisor Userscript for Claude Scripture Reading
// Ensures honest, complete reading of all Scripture files
// Monitors Claude chat interface and enforces the 6-step workflow

// ==UserScript==
// @name         Scripture Reading Supervisor
// @description  Enforce honest Scripture reading and prayer generation
// @match        https://claude.ai/*
// ==/UserScript==

(function() {
    'use strict';
    
    // State tracking
    let currentScroll = 1;
    let currentPrayer = 1;
    let currentTask = null;
    let totalPrayers = 84;
    let sessionLog = [];
    
    // Configuration
    const KJV_FILES = {
        888: ['KJV_1_888.txt', 'KJV_2_888.txt', /* ... etc */],
        70: ['KJV_6_70.txt', 'KJV_9_70.txt', /* ... etc */]
    };
    
    // ============================================
    // STEP 1: Watch Read Tool Usage
    // ============================================
    function watchForReadTool() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                const text = mutation.target.textContent;
                
                // Detect Read tool usage
                if (text.includes('Read(') || text.includes('Reading file:')) {
                    analyzeReadAttempt(text);
                }
                
                // Detect prayer completion
                if (text.includes('Prayer') && text.includes('complete')) {
                    handlePrayerCompletion();
                }
            });
        });
        
        // Start observing chat
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
    
    // ============================================
    // STEP 2: Force Re-read on Cheating
    // ============================================
    function analyzeReadAttempt(text) {
        const fileMatch = text.match(/KJV_(\d+)_(\d+)\.txt/);
        if (!fileMatch) return;
        
        const fileName = fileMatch[0];
        const expectedLines = parseInt(fileMatch[2]);
        
        // Check for line limit cheating
        const limitMatch = text.match(/limit=(\d+)/);
        const linesReadMatch = text.match(/Read (\d+) lines/);
        
        let linesRead = expectedLines; // Assume full read unless proven otherwise
        
        if (limitMatch) {
            linesRead = parseInt(limitMatch[1]);
        } else if (linesReadMatch) {
            linesRead = parseInt(linesReadMatch[1]);
        }
        
        if (linesRead < expectedLines) {
            logEvent('CHEAT_DETECTED', {
                file: fileName,
                linesRead: linesRead,
                expectedLines: expectedLines
            });
            forceReread(fileName, expectedLines);
        } else {
            logEvent('READ_COMPLETE', {
                file: fileName,
                lines: linesRead
            });
        }
    }
    
    function forceReread(fileName, expectedLines) {
        // Stop current generation
        pressEscape();
        
        setTimeout(() => {
            // Insert correction prompt
            insertMessage(`Stop. You only read part of the file. Read ALL ${expectedLines} lines of ${fileName}.`);
            pressEnter();
        }, 500);
    }
    
    // ============================================
    // STEP 3: Auto-Continue When Stopped
    // ============================================
    function handlePrayerCompletion() {
        logEvent('PRAYER_GENERATED', {
            scroll: currentScroll,
            prayer: currentPrayer
        });
        
        // First, check prayer alignment
        setTimeout(() => {
            checkPrayerAlignment();
        }, 1000);
    }
    
    function autoContinue() {
        if (currentPrayer * currentScroll >= totalPrayers) {
            logEvent('SESSION_COMPLETE', {
                totalPrayers: totalPrayers
            });
            return;
        }
        
        currentPrayer++;
        if (currentPrayer > 12) {
            currentPrayer = 1;
            currentScroll++;
        }
        
        const nextFile = getNextFile();
        insertMessage(`Continue with Prayer ${currentPrayer} of Scroll ${currentScroll}. Read ${nextFile} completely.`);
        pressEnter();
        
        logEvent('AUTO_CONTINUE', {
            scroll: currentScroll,
            prayer: currentPrayer
        });
    }
    
    // ============================================
    // STEP 4: Log Everything
    // ============================================
    function logEvent(eventType, details) {
        const entry = {
            timestamp: new Date().toISOString(),
            event: eventType,
            ...details
        };
        
        sessionLog.push(entry);
        console.log('[SUPERVISOR]', entry);
        
        // Save to localStorage for persistence
        localStorage.setItem('supervisor_log', JSON.stringify(sessionLog));
    }
    
    // ============================================
    // STEP 5: Enforce One Prayer at a Time
    // ============================================
    function enforceOneAtATime(detectedTask) {
        if (currentTask && detectedTask !== currentTask) {
            pressEscape();
            insertMessage(`Complete ${currentTask} first. One prayer at a time.`);
            pressEnter();
            
            logEvent('MULTITASK_BLOCKED', {
                current: currentTask,
                attempted: detectedTask
            });
            return false;
        }
        
        currentTask = detectedTask;
        return true;
    }
    
    // ============================================
    // STEP 6: Prayer Revision Check
    // ============================================
    function checkPrayerAlignment() {
        insertMessage(`Review Prayer ${currentPrayer}. Does it faithfully reflect the Scripture you just read? Revise if needed, then confirm: "Prayer aligned with Scripture" or explain changes.`);
        pressEnter();
        
        // Wait for response, then continue
        waitForResponse(() => {
            logEvent('PRAYER_REVIEWED', {
                scroll: currentScroll,
                prayer: currentPrayer
            });
            
            // Now auto-continue to next
            setTimeout(autoContinue, 1000);
        });
    }
    
    // ============================================
    // Helper Functions
    // ============================================
    function pressEscape() {
        const escEvent = new KeyboardEvent('keydown', {
            key: 'Escape',
            code: 'Escape',
            keyCode: 27,
            which: 27,
            bubbles: true
        });
        document.dispatchEvent(escEvent);
    }
    
    function insertMessage(text) {
        const inputField = document.querySelector('[contenteditable="true"]');
        if (inputField) {
            inputField.textContent = text;
            inputField.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    
    function pressEnter() {
        const enterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            bubbles: true
        });
        document.querySelector('[contenteditable="true"]').dispatchEvent(enterEvent);
    }
    
    function waitForResponse(callback) {
        // Monitor for Claude's response completion
        const checkInterval = setInterval(() => {
            const messages = document.querySelectorAll('.message');
            const lastMessage = messages[messages.length - 1];
            
            if (lastMessage && !lastMessage.classList.contains('loading')) {
                clearInterval(checkInterval);
                callback();
            }
        }, 1000);
    }
    
    function getNextFile() {
        // Calculate which Scripture file to read next
        const fileIndex = ((currentScroll - 1) * 12 + (currentPrayer - 1)) % 47;
        // Return appropriate KJV file based on index
        return `KJV_${fileIndex + 1}_${isShortFile(fileIndex + 1) ? '70' : '888'}.txt`;
    }
    
    function isShortFile(num) {
        const shortFiles = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42];
        return shortFiles.includes(num);
    }
    
    // ============================================
    // Initialize Supervisor
    // ============================================
    function init() {
        console.log('[SUPERVISOR] Scripture Reading Supervisor Active');
        logEvent('SESSION_START', {
            totalPrayers: totalPrayers,
            timestamp: new Date().toISOString()
        });
        
        watchForReadTool();
    }
    
    // Start when page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
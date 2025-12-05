### How to Bulk Restore Specific Files in Obsidian Sync

This script solves a specific UI limitation in Obsidian's "Bulk restore" feature where you cannot select all files at once (e.g., with Cmd+A), which is impractical when dealing with hundreds or thousands of files. This situation can occur after a mass file operation, like renaming a folder, which Obsidian Sync may interpret as a mass deletion.

The solution is to use Obsidian's Developer Tools to run a JavaScript snippet that programmatically selects the files you want to restore.

Instructions1. **Navigate to Bulk Restore:** In Obsidian, go to `Settings > Sync`. Under the "Deleted files" section, click the **Bulk restore** button.
2. **Load All Files:** The list of deleted files is virtualized (it only loads a few at a time). To ensure the script can see all files, you **must** scroll to the very bottom of the list. The easiest way is to click inside the list and then **press and hold the `Page Down` key** until you reach the end.
3. **Open Developer Tools:**


- **macOS:** `Cmd + Option + I`
- **Windows/Linux:** `Ctrl + Shift + I`
- A new panel will open. Select the **"Console"** tab.
4. **Run the Script:** Paste the following JavaScript code into the console and press **Enter**.


- **To restore files from a specific folder (e.g., "Archives/"):**


javascript`/** * Selects all checkboxes in the Obsidian "Bulk restore" dialog * for files located within a specific folder (e.g., "Archives/"). */let count = 0;// Find all list items in the modaldocument.querySelectorAll('.modal-content .list-item').forEach(item => {    // Find the part of the item that contains the text    const textElement = item.querySelector('.list-item-part');        // Check if the text content exists and starts with 'Archives/'    if (textElement && textElement.textContent.trim().startsWith('Archives/')) {        // Find the checkbox within this specific list item        const checkbox = item.querySelector('input[type="checkbox"]');                // If a checkbox is found, click it        if (checkbox) {            checkbox.click();            count++;        }    }});// Log the number of items selected for verificationconsole.log(`Clicked ${count} checkboxes.`);`
- **To restore ALL files in the list:**


javascript`/** * Selects ALL checkboxes in the Obsidian "Bulk restore" dialog. * Use this if you want to restore everything in the list. */let count = 0;document.querySelectorAll('.modal-content .list-item input[type="checkbox"]').forEach(checkbox => {    checkbox.click();    count++;});console.log(`Clicked ${count} checkboxes.`);`
5. **Confirm and Restore:** The script will print the number of checkboxes it clicked. Visually confirm that the correct files are selected in the dialog, then click the **"Restore"** button. The sync process will begin restoring your files.

*Note: The HTML class names (`.list-item`, `.list-item-part`) are subject to change with future Obsidian updates. If the script stops working, use the Element Inspector in the Developer Tools to find the new class names and update the script accordingly.*

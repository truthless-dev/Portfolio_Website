// Represent a single Braille cell
class BrailleCell {

    /*
     * Maintain the cell's current state.
     * Each bit represents a single dot, starting from dot1 at the
     * rightmost bit, dot2 one bit to the left, etc.
     * Shouldn't use any bits beyond the 8th (since the largest
     * Braille cell has 8 dots), but in general, no errors are thrown
     * if more are used (though see `asString()`.
    */
    #bits = 0b0;

    /*
     * Calculate the bits corresponding to a single Braille dot,
     * expressed as a number (usually 1-8).
    */
    static #dotBits(dot) {
        return 1 << (dot - 1);
    }

    /*
     * Add one or more dots to the cell.
     * Dots are given in numeric form (e.g., passing `3` will add a
     * dot3 to the cell). Non-numbers are ignored. Adding a dot that
     * has already been added does nothing.
    */
    add(...dots) {
        for (let dot of dots) {
            if (typeof(dot) === "number") {
                this.#bits |= BrailleCell.#dotBits(dot);
            }
        }
    }

    /*
     * Delete one or more dots from the cell.
     * Dots are given in numeric form (e.g., passing `3` will remove
     * dot3 from the cell). Non-numbers are ignored. Deleting a dot
     * that has not yet been added does nothing.
    */
    del(...dots) {
        for (let dot of dots) {
            if (typeof(dot) === "number") {
                this.#bits &= ~BrailleCell.#dotBits(dot);
            }
        }
    }

    /*
     * Remove all dots from the cell.
    */
    clear() {
        this.#bits = 0b0;
    }

    /*
     * Produce a unicode representation of the cell.
     * Note: Any cell with more than 8 dots will output non-Braille
     * characters, as unicode supports only 6- and 8-dot cell chars.
    */
    asString() {
        /*
         * Braille cell characters are in the range 0x2800 - 0x28FF
         * (inclusive), starting with the empty cell. Very fortunately,
         * the characters are ordered from smallest to largest value,
         * assuming values of binary representations of the cells as
         * we implement here. So, we need only add our current state
         * to 0x2800 to get the correct character.
        */
        return String.fromCharCode(0x2800 + this.#bits);
    }

}


// Represent a series of keys that produce Braille cells
class BrailleKeyboard { 

    /*
     * This defines how the user will type Braille on their QWERTY
     * keyboard. The QWERTY key keys correspond to the Braille dot
     * they will produce.
    */
    static #brailleKeys = {
        f: 1, d: 2, s: 3,
        j: 4, k: 5, l: 6,
        a: 7, ";": 8, " ": 0
    };

    /*
     * Track the state of the actual QWERTY keys being pressed so
     * that we can identify multi-dot cells. Values will be `true` if
     * the key is currently down, or `false` if it is up.
    */
    #qwertyKeys = {};

    // The Braille cell which these keys will manipulate.
    #cell;

    constructor(cell) {
        this.#cell = cell;
    }

    /*
     * Produce the unicode representation of the current cell.
    */
    get cell() {
        return this.#cell.asString();
    }

    /*
     * Determine whether a key is a valid Braille key (i.e., one which
     * will produce a Braille dot when typed).
     * `key` is a key name as given by `KeyboardEvent.key`. The check
     * is case-insensitive.
    */
    static isKey(key) {
        return key.toLowerCase() in BrailleKeyboard.#brailleKeys;
    }

    /*
     * Determine whether all Braille keys are currently up (i.e., not
     * pressed).
    */
    #allBrailleKeysUp() {
        for (let key in BrailleKeyboard.#brailleKeys) {
            if (this.#qwertyKeys[key]) {
                return false;
            }
        }
        return true;
    }

    /*
     * Attempt to press a Braille key.
     * Return `true` if the key was pressed successfully; `false`
     * otherwise.
    */
    press(key) {
        key = key.toLowerCase();
        const dot = BrailleKeyboard.#brailleKeys[key];
        if (dot === undefined) {
            // Not a Braille key
            return false;
        }
        if (this.#qwertyKeys[key]) {
            // This key is already pressed--don't repeat
            return true;
        }
        this.#qwertyKeys[key] = true;
        this.#cell.add(dot);
        return true;
    }

    /*
     * Attempt to release a Braille key.
     * Return the string representation of the typed cell if no
     * other Braille keys are pressed. Return `undefined` in all other
     * cases. This enables the typing of multi-dot cells. If a cell
     * was successfully typed, the instance will also update its
     * internal state to allow a fresh cell to be typed.
    */
    release(key) {
        key = key.toLowerCase();
        const dot = BrailleKeyboard.#brailleKeys[key];
        if (dot === undefined) {
            // Not a Braille key
            return undefined;
        }
        if (!this.#qwertyKeys[key]) {
            // The key was not yet pressed
            return undefined;
        }
        this.#qwertyKeys[key] = false;
        if (!this.#allBrailleKeysUp()) {
            // The user's not done making the cell yet
            return undefined;
        }
        const char = this.cell;
        this.#cell.clear();
        return char;
    }

}


const cell = new BrailleCell();
const keyboard = new BrailleKeyboard(cell);
const printableChars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ";

// Get the jQuery object representing the keyboard's input field
function getBrailler() {
    return $("#brailler");
}

/*
 * Determine whether any command keys are down during the event.
 * These include alt, ctrl, and meta. Shift is *not* included, because
 * it generally doesn't cause commands to be run.
*/
function eventHasModifier(event) {
    return event.altKey || event.ctrlKey || event.metaKey;
}

// Handle key-down events on the keyboard input field
function onBraillePress(event) {
    if (eventHasModifier(event)) {
        // Allow normal use of CTRL+A, etc.
        return true;
    }
    const key = event.key;
    if (!keyboard.press(key) && printableChars.search(key) < 0) {
        // Braille does not handle this special key, so pass it on.
        return true;
    }
    // Either this was handled or it's an unhandled alphanum key.
    return false;
}

// Handle key-down events on the keyboard input field
function onBrailleRelease(event) {
    if (eventHasModifier(event)) {
        // Allow normal use of CTRL+A, etc.
        return true;
    }
    const key = event.key;
    char = keyboard.release(key);
    if (char === undefined) {
        // Either key is not handled or the cell is not yet finished.
        if (printableChars.search(key) < 0) {
            // This is a non-alphanum key. Let it be used as normal.
            return true;
        } else {
            // Suppress typing into the input field.
            return false;
        }
    }
    // Append the new cell to the end of the current text.
    const brailler = getBrailler();
    brailler.val(brailler.val() + char);
    return false;
}


$(function() {
    getBrailler().on({keydown: onBraillePress, keyup: onBrailleRelease});
});


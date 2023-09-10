# modified from https://gist.github.com/t510599/986aacc2b96ae323e1ba2a0796ec0024
USB_CODES = {
    0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
    0x0A:"gG", 0x0B:"hH", 0x0C:"iI", 0x0D:"jJ", 0x0E:"kK", 0x0F:"lL",
    0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
    0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1A:"wW", 0x1B:"xX",
    0x1C:"yY", 0x1D:"zZ", 0x1E:"1!", 0x1F:"2@", 0x20:"3#", 0x21:"4$",
    0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
    0x2C:"  ", 0x2D:"-_", 0x2E:"=+", 0x2F:"[{", 0x30:"]}",  0x32:"#~",
    0x33:";:", 0x34:"'\"", 0x36:",<", 0x37:".>", 0x38: "//"
}

BACKSPACE = "←"
DOWN = "↓"
UP = "↑"

key_cache = []

def array(arr):
    ret = []
    for i in range(0, len(arr), 2):
        val = int(arr[i:i+2], 16)
        if val == 0:
            break
        ret.append(val)

    return ret

def handle_keyboard(hid):
    global key_cache

    codes = array(hid[2*2:])
    control_keys = int(hid[2*0:2*0+2], 16)
    shift = control_keys & 0b10 or control_keys & 0b00100000

    keycode_list = []
    input_list = []

    for code in codes:
        char = None

        if not USB_CODES.get(code):
            # newline (Enter) or down arrow - move down
            if code == 0x51 or code == 0x28:
                char = DOWN
            # up arrow - move up
            if code == 0x52:
                char = UP
            # backspace
            if code == 0x2a:
                char = BACKSPACE
        else:
            # select the character based on the Shift key
            if shift:
                char = USB_CODES[code][1]
            else:
                char = USB_CODES[code][0]

        if not char:
            continue

        if code not in key_cache:
            input_list.append(char)

        keycode_list.append(code)

    key_cache = keycode_list

    return input_list
    
DEVICE_KBOAD = "10"

output_buffer = [""]
current_line = 0

# extract data first
# tshark -r release.pcapng -T fields -E separator=, -e usb.device_address -e usbhid.data "usb.device_address == {DEVICE_KBOAD} && usb.bus_id == 1 && usb.transfer_type == 1 && usb.urb_type == 'C'" > time.txt
with open("time.txt") as f:
    data = f.readlines()

for l in data:
    device, raw_data = l.split(",")

    if device == DEVICE_KBOAD:
        res = handle_keyboard(raw_data)
        for char in res:
            if char == UP:
                current_line = max(current_line - 1, 0)
            elif char == DOWN:
                current_line = current_line + 1
                if len(output_buffer) - 1 < current_line:
                    output_buffer.append("")
            elif char == BACKSPACE:
                output_buffer[current_line] = output_buffer[current_line][:-1]
            else:
                output_buffer[current_line] += char

for line in output_buffer:
    print(line)
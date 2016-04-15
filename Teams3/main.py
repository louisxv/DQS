"""
pygest.py
A simple Python GUI tutorial application for processing file hashes.
Final Version
blog.agupieware.com
"""

import tkinter
import tkinter.filedialog as fd
import hashlib
import logging

title = "PyGest"

class View():
    """
    The main view class for the PyGest tkinter interface.
    """
    def __init__(self, root_object):
        self.root = root_object
        self.mainframe = None
        self.filePath = None
        self.set_up()

    def set_up(self):
        """
        Run necessary view and widget configuration methods.
        """
        self.configure_root()
        self.configure_mainframe()
        self.configure_banner()
        self.configure_inputs()
        self.configure_outputs()
        self.configure_buttons()

    def configure_root(self):
        """
        Configure the root window of the app via the self.root attribute.
        """
        logging.info("configure_root method called...")
        # self.root.minsize(200, 200)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def configure_mainframe(self):
        """
        Configure the main frame in the root cell with grid geometry manager.
        """
        logging.info("We are in the configure_mainframe method")
        self.mainframe = tkinter.Frame(self.root, background='white')
        self.mainframe.grid(column=0, row=0, sticky=('N', 'S', 'E', 'W'))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=1)
        self.mainframe.rowconfigure(3, weight=1)

    def configure_banner(self):
        """
        Configure the header banner for the app with a simple tkinter label.
        """
        logging.info("We are in the banner method")
        banner = tkinter.Label(self.mainframe, background='black', text="PyGest Tutorial App", font=('Futura', 32), fg='white')
        banner.grid(row=0, column=0, sticky=('N', 'S', 'E', 'W'), padx=10, pady=10)

    def configure_inputs(self):
        """
        Configure app input objects: file path, hash value, radio buttons.
        """
        logging.info("We're in the configure_inputs method")
        inputs_frame = tkinter.Frame(self.mainframe, background='white', borderwidth=2, relief='flat')
        inputs_frame.grid(row=1, column=0, sticky=('N', 'S', 'E', 'W'))
        inputs_frame.columnconfigure(0, weight=1)
        inputs_frame.columnconfigure(1, weight=1)
        inputs_frame.columnconfigure(2, weight=1)
        inputs_frame.rowconfigure(0, weight=1)
        inputs_frame.rowconfigure(1, weight=1)

        filepath_label = tkinter.Label(inputs_frame, text="File Name:")
        filepath_label.grid(row=0, column=0, sticky='E')

        self.file_entry = tkinter.Entry(inputs_frame)
        self.file_entry.bind("<Button-1>", self.chooseFileName)
        self.file_entry.grid(row=0, column=1, sticky=('E', 'W'))

        self.radio_var = tkinter.StringVar()
        self.radio_var.set('sha1')
        sha1 = tkinter.Radiobutton(inputs_frame, text="sha1", variable=self.radio_var, value='sha1')
        sha1.grid(row=0, column=2)

        digest_label = tkinter.Label(inputs_frame, text="Compare Digest:")
        digest_label.grid(row=1, column=0,  sticky='E')

        self.digest_entry = tkinter.Entry(inputs_frame)
        self.digest_entry.grid(row=1, column=1, sticky=('E', 'W'))

        md5 = tkinter.Radiobutton(inputs_frame, text="md5", variable=self.radio_var, value='md5')
        md5.grid(row=1, column=2)


    def chooseFileName(self, event):
        """
        Controls file path pop up dialog on click of entry field.
        """
        logging.info("Choose File Name method called.")
        self.filePath = fd.askopenfilename(title="Choose File to Hash")
        logging.info("File path: " + self.filePath)
        self.file_entry.insert(0, self.filePath)

    def configure_outputs(self):
        """
        Configure output widgets: hash value, match value.
        """
        logging.info("We're in the configure_outputs method")
        outputs_frame = tkinter.Frame(self.mainframe, borderwidth=2, relief='flat')
        outputs_frame.grid(row=2, column=0, sticky=('N', 'S', 'E', 'W'))
        outputs_frame.rowconfigure(0, weight=1)
        outputs_frame.rowconfigure(1, weight=1)
        outputs_frame.columnconfigure(0, weight=1)
        outputs_frame.columnconfigure(1, weight=1)
        outputs_frame.columnconfigure(2, weight=1)

        hash_value_label = tkinter.Label(outputs_frame, text="Hash Value:")
        hash_value_label.grid(row=0, column=0, sticky='E')

        self.hash_value = tkinter.StringVar()
        self.hash_value.set("")

        self.hash_value_entry = tkinter.Entry(outputs_frame, state='readonly', readonlybackground='white', fg='black')
        self.hash_value_entry.config(textvariable=self.hash_value, relief='flat', highlightthickness=0)
        self.hash_value_entry.grid(row=0, column=1, columnspan=2, sticky=('W', 'E'))

        result_label = tkinter.Label(outputs_frame, text="Result:")
        result_label.grid(row=1, column=0, sticky='E')

        self.result_var = tkinter.StringVar()
        self.result_var.set("")

        result_display_label = tkinter.Label(outputs_frame, textvariable=self.result_var)
        result_display_label.grid(row=1, column=1, sticky=('W'))

    def configure_buttons(self):
        """
        Configure button frame and two buttons: hash and clear.
        """
        logging.info("We're in the configure buttons method.")
        buttons_frame = tkinter.Frame(self.mainframe, borderwidth=2, relief='flat')
        buttons_frame.grid(row=3, column=0,  sticky=('N', 'S', 'E', 'W'))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.rowconfigure(0, weight=1)
        buttons_frame.rowconfigure(1, weight=1)

        hash_button = tkinter.Button(buttons_frame, text='Hash', relief='raised', command=self.runHash)
        hash_button.grid(row=0, column=0, sticky=('N', 'S', 'E', 'W'))

        clear_button = tkinter.Button(buttons_frame, text='Clear', relief='raised', command=self.clear)
        clear_button.grid(row=1, column=0, sticky=('N', 'S', 'E', 'W'))

    def runHash(self):
        """
        Contains functionality to run the hash function.
        """
        logging.info("Hash button pressed.")
        path = self.filePath
        hash_func = self.radio_var.get()
        logging.info("File path: {}".format(path))
        logging.info("Hash func: {}".format(hash_func))
        digest = processDigest(path, hash_func)
        logging.info("Hash digest: {}".format(digest))

        self.hash_value.set(digest)
        new_hash_value_entry = self.hash_value_entry.get()
        logging.info("New Hash Value Entry: {}".format(new_hash_value_entry))

        user_input_digest_value = self.digest_entry.get()

        if user_input_digest_value == "":
            self.result_var.set("Done")
        elif user_input_digest_value == digest:
            self.result_var.set("Success! Digest match.")
        else:
            self.result_var.set("Fail! No match.")


    def clear(self):
        """
        Clears all input and output fields.
        """
        logging.info("Clear button pressed.")
        self.hash_value.set("")
        self.result_var.set("")
        self.digest_entry.delete(0, 'end')
        self.file_entry.delete(0, 'end')


def processDigest(path, hash_type):
    """
    Run hash function of type hash_type on file at path. Return digest.
    """
    if hash_type == "md5":
        hashFunc = hashlib.md5()
    else:
        hashFunc = hashlib.sha1()

    blockSize = 65535
    try:
        with open(path, 'rb') as target:
            buf = target.read(blockSize)
            while len(buf) > 0:
                hashFunc.update(buf)
                buf = target.read(blockSize)
        digested = hashFunc.hexdigest()
        return digested
    except (IOError, TypeError) as error:
        logging.debug("Error in hash func: {}".format(error))

def main():
    """
    Main function to run the PyGest GUI application.
    """
    logging.basicConfig(format='[%(asctime)s] ln:%(lineno)d %(levelname)s: %(message)s', datefmt='%I:%M:%s', level=logging.DEBUG)
    logging.info('{} app started. Logger running.'.format(title))

    # Declare the tkinter Tk() object as root
    root = tkinter.Tk()

    # Pass in its title
    root.title(title)

    # Pass the root object to our main View() class
    gui = View(root)

    # Run the Tk() object's main loop
    root.mainloop()

if __name__ == "__main__":
    main()

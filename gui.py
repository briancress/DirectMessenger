"""Module for GUI"""
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
import os
import platform
import subprocess
import Profile
import ds_messenger
import time


class Body(tk.Frame):
    """Class for body"""
    def __init__(self, root, recipient_selected_callback=None):
        """Initialize Values"""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """Selects node"""
        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)
        except IndexError:
            pass

    def reset_contacts(self):
        """Resets contacts"""
        self.posts_tree.delete(*self.posts_tree.get_children())

    def insert_contact(self, contact: str):
        """Inserts contacts"""
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """Inserts contact tree"""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """Inserts user message"""
        self.entry_editor.insert('end', message + '\n', 'entry-right')
        # self.entry_editor.yview_moveto(1)

    def insert_contact_message(self, message: str):
        """Inserts contact message"""
        self.entry_editor.insert('end', message + '\n', 'entry-left')
        # self.entry_editor.yview_moveto(1)

    def get_text_entry(self) -> str:
        """Gets entry"""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Sets text entry"""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Draw"""
        posts_frame = tk.Frame(master=self, width=250, bg='SteelBlue1')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg='lightsalmon')
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg='lightsalmon')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg='powderblue')
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Footer class"""
    def __init__(self, root, send_callback=None):
        """Initialize values"""
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()
        self.body = Body(root)

    def send_click(self):
        """Sends click"""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draws widget"""
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click, bg='pink')
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.", fg='cyan2', bg='light salmon')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """New contact class"""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Initialize"""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """Body widget"""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address", bg='turqoise')
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        # self.password...

    def apply(self):
        """Gets entries"""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """Class for main application"""
    def __init__(self, root):
        """Initialize values"""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.new_file_path = None
        self.plat = platform.system()
        self.timer = None
        self.errorbox = False
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = ... continue!

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        # self.body.insert_contact() # adding one example student.

    def friends_list(self):
        """Inserts friend contacts"""
        self.body.reset_contacts()
        # self.check_new()
        try:
            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            for i in profile.friends:
                self.body.insert_contact(i)
        except Profile.DsuFileError:
            pass
        except Profile.DsuProfileError:
            pass

    def send_message(self):
        """Sends message"""
        # You must implement this!
        text = self.body.get_text_entry()
        # print(text)
        self.body.set_text_entry('')
        profile = Profile.Profile()
        try:
            profile.load_profile(self.new_file_path)
            message_send = ds_messenger.DirectMessenger(profile.dsuserver, profile.username, profile.password)
            if message_send.send(text, self.recipient) is True:
                # self.body.insert_user_message(text)
                timestamp = str(time.time())
                sent_message = Profile.SentMessage(text, self.recipient, timestamp)
                profile.add_sent_message(sent_message)
                profile.save_profile(self.new_file_path)
                self.errobox = False
            else:
                # print('Didnt send')
                tk.messagebox.showerror("Error", "Couldn't send message, check internet or IP address (no newlines allowed)")
                self.errorbox = True
        except TypeError:
            tk.messagebox.showerror("Error", "Must load profile or choose recipient before sending messages")

    def add_contact(self):
        """Adds contact"""
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        self.new_contact_window = tk.Toplevel(self.root)
        tk.Label(self.new_contact_window, text="New Contact").grid(row=0, column=0)
        contact_entry = tk.Entry(self.new_contact_window)
        contact_entry.grid(row=0, column=1)
        tk.Button(self.new_contact_window, text="Save", command=self.new_contact_saver).grid(row=4, column=0, columnspan=2)

        self.contact_entry = contact_entry

    def new_contact_saver(self):
        """Saves new contact"""
        new_contact = self.contact_entry.get()
        # print(new_contact)
        self.new_contact_window.destroy()
        profile = Profile.Profile()
        profile.load_profile(self.new_file_path)
        profile.add_friend(new_contact)
        profile.save_profile(self.new_file_path)
        self.friends_list()

    def recipient_selected(self, recipient):
        """Shows selected recipient"""
        self.body.entry_editor.delete('1.0', tk.END)
        self.recipient = recipient
        self.add_new_received()

    def configure_server(self):
        """Configures server"""
        self.configure_server_window = tk.Toplevel(self.root)
        tk.Label(self.configure_server_window, text="Configure").grid(row=0, column=0)
        configure_server = tk.Entry(self.configure_server_window)
        configure_server.grid(row=0, column=1)

        tk.Label(self.configure_server_window, text="Username").grid(row=0, column=0)
        c_username_entry = tk.Entry(self.configure_server_window)
        c_username_entry.grid(row=0, column=1)

        tk.Label(self.configure_server_window, text="Password").grid(row=1, column=0)
        c_password_entry = tk.Entry(self.configure_server_window)
        c_password_entry.grid(row=1, column=1)

        tk.Label(self.configure_server_window, text="Bio").grid(row=2, column=0)
        c_bio_entry = tk.Entry(self.configure_server_window)
        c_bio_entry.grid(row=2, column=1)

        tk.Label(self.configure_server_window, text="IP Address").grid(row=3, column=0)
        c_dsuserver_address_entry = tk.Entry(self.configure_server_window)
        c_dsuserver_address_entry.grid(row=3, column=1)

        tk.Button(self.configure_server_window, text="Save", command=self.configure_server_saver).grid(row=4, column=0, columnspan=2)

        self.c_username_entry = c_username_entry
        self.c_password_entry = c_password_entry
        self.c_bio_entry = c_bio_entry
        self.c_server_entry = c_dsuserver_address_entry

    def configure_server_saver(self):
        """Saves new variables"""
        c_username = self.c_username_entry.get()
        c_password = self.c_password_entry.get()
        c_bio = self.c_bio_entry.get()
        c_server = self.c_server_entry.get()
        self.configure_server_window.destroy()

        profile = Profile.Profile()
        profile.load_profile(self.new_file_path)
        if c_username != '':
            profile.username = c_username
        if c_password != '':
            profile.password = c_password
        if c_bio != '':
            profile.bio = c_bio
        if c_server != '':
            profile.dsuserver = c_server
        profile.save_profile(self.new_file_path)

    def publish(self, message: str):
        """Publishes"""
        # You must implement this!
        pass

    def check_new(self):
        """Checks for new people"""
        # You must implement this!
        if self.new_file_path != None:
            self.friends_list()
            profile = Profile.Profile()
            try:
                profile.load_profile(self.new_file_path)
                new = ds_messenger.DirectMessenger(profile.dsuserver, profile.username, profile.password)
                new_messages = new.retrieve_new()
                if new_messages is not False:
                    profile.save_profile(self.new_file_path)
                    for i in new_messages:
                        prof_message = Profile.Message(i.message, i.recipient, i.timestamp)
                        profile.add_friend(i.recipient)
                        profile.add_message(prof_message)
                    profile.save_profile(self.new_file_path)
                    self.errorbox = False
                else:
                    if self.errorbox == False:
                        # print('Couldn\'t retrieve new messages')
                        tk.messagebox.showerror("Error", "Invalid username or no internet, Loaded past messages")
                        self.errorbox = True
            except Profile.DsuFileError:
                pass
            except Profile.DsuProfileError:
                pass

    def _draw(self):
        """draws widget"""
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_file.config(activeforeground='skyblue', foreground='salmon')
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.config(activeforeground='skyblue', foreground='salmon')
        menu_file.add_command(label='New', command=self.file_creator)
        menu_file.add_command(label='Open...', command=self.file_opener)
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        settings_file.config(activeforeground='skyblue', foreground='salmon')
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

    def file_opener(self):
        """Opens file"""
        try:
            path = filedialog.askopenfilename(parent=self.root)
            if not path.endswith('.dsu'):
                tk.messagebox.showerror("Error", "Invalid file path, not dsu file")
            else:
                self.new_file_path = path

            self.friends_list()
            self.add_new_received()
        except Profile.DsuFileError:
            pass
        except TypeError:
            pass

    def file_creator(self):
        """Creates file"""
        if self.plat == 'Windows':
            path = filedialog.asksaveasfilename(defaultextension='.dsu', filetypes=[('DSU files', '.dsu')])
            self.new_file_path = path
            # print(self.new_file_path)
            if path:
                open(path, 'a').close()
                # os.startfile(path)
        else:
            path = filedialog.asksaveasfilename(defaultextension='.dsu', filetypes=[('DSU files', '.dsu')])
            self.new_file_path = path
            # print(self.new_file_path)
            if path:
                open(path, 'a').close()
                # subprocess.call('open', path)
        # Create a new window to prompt for user info
        self.user_window = tk.Toplevel(self.root)

        # Add Labels, Entries, and Buttons to the new window
        tk.Label(self.user_window, text="Username").grid(row=0, column=0)
        username_entry = tk.Entry(self.user_window)
        username_entry.grid(row=0, column=1)

        tk.Label(self.user_window, text="Password").grid(row=1, column=0)
        password_entry = tk.Entry(self.user_window)
        password_entry.grid(row=1, column=1)

        tk.Label(self.user_window, text="Bio").grid(row=2, column=0)
        bio_entry = tk.Entry(self.user_window)
        bio_entry.grid(row=2, column=1)

        tk.Label(self.user_window, text="IP Address").grid(row=3, column=0)
        dsuserver_address_entry = tk.Entry(self.user_window)
        dsuserver_address_entry.grid(row=3, column=1)

        tk.Button(self.user_window, text="Save", command=self.upd_saver).grid(row=4, column=0, columnspan=2)

        # Save the Entry widgets as instance variables so you can access their values later
        self.username_entry = username_entry
        self.password_entry = password_entry
        self.bio_entry = bio_entry
        self.server_entry = dsuserver_address_entry
        try:
            self.friends_list()
            self.add_new_received()
        except Profile.DsuFileError:
            pass
        except Profile.DsuProfileError:
            pass

    def upd_saver(self):
        """Saves username pass and bio"""
        self.username = self.username_entry.get()
        # print(self.username)
        self.password = self.password_entry.get()
        # print(self.password)
        self.bio = self.bio_entry.get()
        # print(self.bio)
        self.server = self.server_entry.get()
        # print(self.server)
        self.user_window.destroy()
        
        self.dsu_profile_save()

    def dsu_profile_save(self):
        """Saves dsu profile"""
        try:
            profile = Profile.Profile()
            profile.save_profile(self.new_file_path)
            profile.username = self.username
            profile.password = self.password
            profile.bio = self.bio
            profile.dsuserver = self.server
            profile.save_profile(self.new_file_path)
        except Profile.DsuFileError:
            pass

    def add_new_received(self):
        """Adds new received"""
        cur_pos = self.body.entry_editor.yview()[0]
        self.body.entry_editor.delete('1.0', tk.END)
        self.check_new()
        try:
            profile = Profile.Profile()
            profile.load_profile(self.new_file_path)
            all_messages = []
            for i in profile._messages:
                if i['sender'] == self.recipient:
                    all_messages.append(i)
            for i in profile._sent_messages:
                if i['to'] == self.recipient:
                    all_messages.append(i)
            all_messages.sort(key=lambda x: x['timestamp'])
            for i in all_messages:
                try:
                    l = i['sender']
                    self.body.insert_contact_message(i['message'])
                except KeyError:
                    try:
                        self.body.insert_user_message(i['message'])
                    except KeyError:
                        pass
        except Profile.DsuFileError:
            pass
        except Profile.DsuProfileError:

            if self.errorbox == False:
                # print('Couldn\'t retrieve new messages')
                tk.messagebox.showerror("Error", "Invalid DSU File contents")
                self.errorbox = True
            pass

        if self.timer is not None:
            self.root.after_cancel(self.timer)
        # self.body.update_idletasks()
        self.body.entry_editor.yview_moveto(cur_pos)
        self.timer = self.root.after(2000, self.add_new_received)


def main():
    """Main function"""
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()

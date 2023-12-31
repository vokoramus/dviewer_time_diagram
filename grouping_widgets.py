import tkinter as tk


class ListFrame(tk.Frame):
    def __init__(self, master, items=None):
        super().__init__(master)
        if items is None:
            items = []
        self.list = tk.Listbox(self)
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL,
                                   command=self.list.yview)

        self.list.config(yscrollcommand=self.scroll.set,
                         exportselection=False,  # for independent focus
                         )
        self.list.insert(0, *items)
        self.list.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

    def get_selection(self):
        index = self.list.curselection()
        if index:
            value = self.list.get(index)
            # self.list.delete(index)
            return value

    def del_item(self, label):
        index = self.list.get(0, tk.END).index(label)
        if index:
            self.list.delete(index)
            return

    def insert_item(self, channel, value, value2):
        pair = f'{channel} ({value}%__%{value2})'
        self.list.insert(tk.END, pair)

    def insert_reserve(self, reserve_name):
        self.list.insert(tk.END, reserve_name)


class App(tk.Tk):
    def __init__(self, events_list, channels_dict):
        super().__init__()
        self.var = tk.StringVar()
        self.txt = tk.Entry(self, textvariable=self.var)
        self.var2 = tk.StringVar()
        self.txt2 = tk.Entry(self, textvariable=self.var2)

        self.frame_a = ListFrame(self, events_list)
        self.frame_a2 = ListFrame(self, events_list)
        self.frame_b = ListFrame(self)
        self.btn_pair = tk.Button(self, text=">>",
                                  command=self.move)
        self.btn_add_reserve = tk.Button(self, text="res",
                                  command=self.add_reserve)

        self.btn_end = tk.Button(self, text="End",
                                 command=self.exit)

        self.txt.pack(side=tk.TOP)
        self.txt2.pack(side=tk.TOP)
        self.frame_a.pack(side=tk.LEFT, padx=10, pady=10)
        self.frame_a2.pack(side=tk.LEFT, padx=10, pady=10, fill='y')
        self.frame_b.pack(side=tk.RIGHT, padx=10, pady=10, fill='y')
        self.btn_pair.pack(expand=True, ipadx=5)
        self.btn_add_reserve.pack(expand=True, ipadx=5)
        self.btn_end.pack(expand=True, ipadx=5)
        self.channels_dict = channels_dict

    def move(self):
        value = self.frame_a.get_selection()
        value2 = self.frame_a2.get_selection()
        channel = self.var.get()
        if value and value2 and value != value2 \
                and value != '___' and value2 != '___' \
                and channel not in self.channels_dict.keys() \
                and len(channel):
            # self.var.set(value)
            self.frame_b.insert_item(channel, value, value2)
            self.frame_a.del_item(value)
            self.frame_a.del_item(value2)
            self.frame_a2.del_item(value)
            self.frame_a2.del_item(value2)
            channel_dict = {0: value, 1: value2}
            self.channels_dict[channel] = channel_dict

    def add_reserve(self):
        reserve_name = self.var2.get()
        if len(reserve_name):
            self.frame_a.insert_reserve(reserve_name)
            self.frame_a2.insert_reserve(reserve_name)


    def exit(self):
        self.quit()



if __name__ == "__main__":
    events_list = ["___", "Январь", "Февраль", "Март", "Апрель",
                   "Май", "Июнь", "Июль", "Август", "Сентябрь",
                   "Октябрь", "Ноябрь", "Декабрь"]
    channels_dict = {}
    app = App(events_list, channels_dict)
    app.mainloop()

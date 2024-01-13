def ListAppend(ListX):
        def decorator(method):
            def wrapper(*args, **kwargs):
                result = method(*args, **kwargs)
                ListX.append(result)
                return result
            return wrapper
        return decorator

[([<PIL.ImageTk.PhotoImage object at 0x0000024374C2B590>,
   <PIL.ImageTk.PhotoImage object at 0x0000024378967EC0>,
   <PIL.ImageTk.PhotoImage object at 0x0000024374C2B500>,
   <PIL.ImageTk.PhotoImage object at 0x0000024374C2B560>],
   
   [<PIL.ImageTk.PhotoImage object at 0x0000024378988770>,
    <PIL.ImageTk.PhotoImage object at 0x00000243789893D0>,
    <PIL.ImageTk.PhotoImage object at 0x00000243789894C0>,
    <PIL.ImageTk.PhotoImage object at 0x0000024378989520>,
    <PIL.ImageTk.PhotoImage object at 0x0000024378989610>,
    <PIL.ImageTk.PhotoImage object at 0x0000024374AA8E00>,
    <PIL.ImageTk.PhotoImage object at 0x0000024378989490>],
    
    [<PIL.ImageTk.PhotoImage object at 0x00000243789893A0>,
     <PIL.ImageTk.PhotoImage object at 0x0000024374AFE540>,
     <PIL.ImageTk.PhotoImage object at 0x00000243789896A0>,
     <PIL.ImageTk.PhotoImage object at 0x0000024378989730>,
     <PIL.ImageTk.PhotoImage object at 0x0000024378989850>,
     <PIL.ImageTk.PhotoImage object at 0x0000024378988EC0>,
     <PIL.ImageTk.PhotoImage object at 0x0000024374BEC1A0>],
     
     [<PIL.ImageTk.PhotoImage object at 0x0000024378989700>,
      <PIL.ImageTk.PhotoImage object at 0x00000243789897C0>,
      <PIL.ImageTk.PhotoImage object at 0x0000024378989A00>,
      <PIL.ImageTk.PhotoImage object at 0x0000024378989910>,
      <PIL.ImageTk.PhotoImage object at 0x0000024378989970>,
      <PIL.ImageTk.PhotoImage object at 0x0000024372A99730>,
      <PIL.ImageTk.PhotoImage object at 0x00000243789899D0>],
      
      [<PIL.ImageTk.PhotoImage object at 0x0000024378989CA0>,
       <PIL.ImageTk.PhotoImage object at 0x0000024378989D60>,
       <PIL.ImageTk.PhotoImage object at 0x0000024378989C70>,
       <PIL.ImageTk.PhotoImage object at 0x0000024378989D30>,
       <PIL.ImageTk.PhotoImage object at 0x0000024378989DC0>,
       <PIL.ImageTk.PhotoImage object at 0x0000024374C417C0>,
       <PIL.ImageTk.PhotoImage object at 0x0000024378989EE0>])]
from colorprt import colorstr, ColorprtConfig, Fore
lang_output_config = ColorprtConfig(foreground=Fore.BLUE)
a = str(colorstr('asdfasdf', config=lang_output_config))
print(a)
pass
        

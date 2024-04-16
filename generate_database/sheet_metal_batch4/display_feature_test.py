from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import write_step_file
from feature_test import Compound


new_compound, feature0, feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8, feature9, \
    feature10, feature11, feature12, feature13, feature14, feature15, feature16, feature17, feature18, feature19, \
    feature20, feature21, feature22, feature23, feature24, feature25, feature26, feature27, feature28 \
    = Compound(50, 90, 0.8, 3, 44, 4, 5, 3, 28, 2, 30, 60, 3, 25, 33, 2.5, 17, 50).compound()

display, start_display, add_menu, add_function_to_menu = init_display()  # 初始化
display.DisplayShape(new_compound, update=True)
write_step_file(new_compound, f'D:\\Users Files\\Layout\\file9.step')

display.FitAll()
start_display()

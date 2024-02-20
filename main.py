import os, subprocess, time

from image_tagger import ASCIIImageTagger
from get_key import getch
from image_viewer import ASCIIImageViewer, rgb_to_ansi_color_ascii

if __name__ == "__main__":
    viewer = ASCIIImageTagger(filepath="data/Aventurien_Master_5125x8200.png")
    viewer.load_image()
    viewer.center()
    viewer.move_factor = 3
    viewer.brush.set_radius(3)


    while True:
        os.system("cls" if os.name == 'nt' else "clear")
        viewer.update_buffer()
        viewer.print_display_buffer(transform=rgb_to_ansi_color_ascii)
        print(viewer)

        key = getch()
        if key == 'q':  # Press 'q' to exit the loop
            break
        elif key == 'w':
            viewer.move("up")
        elif key == 'a':
            viewer.move("left")
        elif key == 's':
            viewer.move("down")
        elif key == 'd':
            viewer.move("right")
        elif key == "+":
            viewer.brush.set_radius(viewer.brush.radius + 1)
        elif key == "-":
            viewer.brush.set_radius(viewer.brush.radius - 1)
        elif key == "y":
            viewer.move_factor -= 1
        elif key == "x":
            viewer.move_factor += 1
        elif key == "b":
            print(viewer.get_brush_bitmask_position_list())
            input("Enter to continue")
        elif key == 't':
            tag = input("Add Tag: ")
            viewer.add(tag, viewer.get_brush_bitmask_position_list())
        elif key == 'T':
            print(f"List of Tags: {viewer.all_tags}")
            input("Enter to continue")
        elif key == 'r':
            tag = input("Remove Tag: ")
            viewer.remove(tag, viewer.get_brush_bitmask_position_list())
        elif key == "m":
            print("Show mask")
            #viewer.show_mask()
        elif key == "M":
            print("Make mask")
            #viewer.make_mask()
        elif key == "\t":
            viewer.set_random()

        time.sleep(0.01)

    # Save and Exit
    viewer.save()

    subprocess.run('stty sane', shell=True)
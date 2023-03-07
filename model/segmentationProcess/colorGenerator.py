import colorsys

def GenerateColors(segments):
    start_hue = 0
    hue_increment = 360 / segments

    colors = []

    for i in range(segments):
        hue = start_hue + i * hue_increment
        hsl_color = (hue, 60, 60)
        rgb_color = tuple(round(i * 255) for i in colorsys.hls_to_rgb(hsl_color[0]/360, hsl_color[1]/100, hsl_color[2]/100))
        colors.append(rgb_color)

    return colors

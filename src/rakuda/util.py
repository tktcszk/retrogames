def rectangles_overlap(a, b):
    # a, b はそれぞれ4点のタプル（順序は (x1, y1), (x2, y1), (x1, y2), (x2, y2)）
    
    # a の x, y の最小・最大を求める
    ax1 = min(a[0][0], a[2][0])
    ax2 = max(a[1][0], a[3][0])
    ay1 = min(a[0][1], a[1][1])
    ay2 = max(a[2][1], a[3][1])

    # b の x, y の最小・最大を求める
    bx1 = min(b[0][0], b[2][0])
    bx2 = max(b[1][0], b[3][0])
    by1 = min(b[0][1], b[1][1])
    by2 = max(b[2][1], b[3][1])

    # 一方の矩形がもう一方の外側に完全にある場合、重ならない
    if ax2 < bx1 or bx2 < ax1:
        return False
    if ay2 < by1 or by2 < ay1:
        return False

    # 上記で除外されなければ、重なっている
    return True

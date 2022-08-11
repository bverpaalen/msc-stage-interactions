import shapes
import circle_point_selection as PS

circle = shapes.Circle()
print(circle.random_point_in_circle())

print(PS.bestNPointSelection((circle,1,1),(0,0)))
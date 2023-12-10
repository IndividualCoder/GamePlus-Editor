            ray = boxcast(e.world_position, e.right, 3, debug=True)
            # print(ray.distance, ray2.distance)
            intersection_marker.world_position = ray.world_point
            intersection_marker.visible = ray.hit
            if ray.hit:
                d.color = color.azure
                print("hit")
            else:
                d.color = color.orange
                print("NObe")

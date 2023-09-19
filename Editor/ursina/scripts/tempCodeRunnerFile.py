    print(norms)
    from ursina import *
    app = Ursina()
    m = Mesh(vertices=vertices)
    m.generate_normals()
    e = Entity(model=m)
    # print(e.normals)
    if e.normals:
        verts = list()
        for i in range(len(e.vertices)):
            verts.append(e.vertices[i])
            verts.append(Vec3(e.vertices[i][0], e.vertices[i][1], e.vertices[i][2])
                + Vec3(e.normals[i][0], e.normals[i][1], e.normals[i][2])*2)
    
        lines=Entity(model=Mesh(verts, mode='line'))
    # e.shader = 'shader_normals'
    EditorCamera()
    app.run()

import numpy as np

from gridding.fractured import split_grid
from core.grids import structured

def test_split_fracture():
    """ Check that no error messages are created in the process of creating a
    split_fracture.
    """
    n = 10
    g = structured.CartGrid([n,n])
    g.compute_geometry()
    frac_tag = np.logical_and(np.logical_and(g.face_centers[1,:]==n/2,
                                             g.face_centers[0,:]>n/4),
                              g.face_centers[0,:]<3*n/4)
    h = g.copy()
    h = split_grid.split_fracture(h,frac_tag)
    # Check that correct number of faces are added
    assert h.num_faces == g.num_faces + sum(frac_tag)
    assert h.num_faces == h.face_nodes.shape[1]
    assert h.cell_faces.shape[0] == h.num_faces
    assert h.cell_faces.shape[1] == g.num_cells
    assert h.num_cells == g.num_cells
    # Check that correct number of nodes are added
    assert h.num_nodes == g.num_nodes + sum(frac_tag)-1
    assert h.num_nodes == h.face_nodes.shape[0]
    # check that no faces are hanging
    b = np.abs(h.cell_faces).sum(axis=1).A.ravel(1)==0
    assert np.any(b) == False
    # check that internal boundaries are added
    bndr_g = g.get_boundary_faces()
    bndr_h = h.get_boundary_faces()
    assert bndr_g.size ==  bndr_h.size - 2*np.sum(frac_tag)


def test_intersecting_fracture():
    n = 10
    g = structured.CartGrid([n,n])
    g.compute_geometry()
    frac_tag1 = np.logical_and(np.logical_and(g.face_centers[1,:]==n/2,
                                              g.face_centers[0,:]>n/4),
                               g.face_centers[0,:]<3*n/4)

    frac_tag2 = np.logical_and(np.logical_and(g.face_centers[0,:]==n/2,
                                          g.face_centers[1,:]>n/4),
                           g.face_centers[1,:]<3*n/4)
    f = split_grid.Fracture(g)
    f.add_tag(frac_tag1)
    f.add_tag(frac_tag2)
    f.set_tips(g)
    h = g.copy()
    h = split_grid.split_grid(h,f)
    # check that no nodes are hanging
    # Check that correct number of faces are added
    assert h.num_faces == g.num_faces + np.sum(f.tag)
    assert h.num_faces == h.face_nodes.shape[1]
    assert h.cell_faces.shape[0] == h.num_faces
    assert h.cell_faces.shape[1] == g.num_cells
    assert h.num_cells == g.num_cells
    # check that correct number of nodes are added
    assert h.num_nodes == h.face_nodes.shape[0]
    # check that no faces are hanging
    b = np.abs(h.cell_faces).sum(axis=1).A.ravel(1)==0
    assert np.any(b) == False
    # check that internal boundaries are added
    bndr_g = g.get_boundary_faces()
    bndr_h = h.get_boundary_faces()
    assert bndr_g.size ==  bndr_h.size - 2*np.sum(f.tag)
    
if __name__ == '__main__':
    test_split_fracture()

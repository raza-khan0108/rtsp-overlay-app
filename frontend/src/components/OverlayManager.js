import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './OverlayManager.css';

const OverlayManager = () => {
  const [overlays, setOverlays] = useState([]);
  const [formData, setFormData] = useState({
    content: '',
    type: 'text',
    x: 0,
    y: 0,
    width: 100,
    height: 50
  });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:5000/api/overlays';

  // Fetch all overlays on component mount
  useEffect(() => {
    fetchOverlays();
  }, []);

  const fetchOverlays = async () => {
    try {
      setLoading(true);
      const response = await axios.get(API_URL);
      setOverlays(response.data.overlays || []);
    } catch (error) {
      console.error('Error fetching overlays:', error);
      alert('Failed to fetch overlays');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'x' || name === 'y' || name === 'width' || name === 'height' 
        ? parseInt(value) || 0 
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.content.trim()) {
      alert('Content is required');
      return;
    }

    try {
      if (editingId) {
        // Update existing overlay
        await axios.put(`${API_URL}/${editingId}`, formData);
        alert('Overlay updated successfully');
        setEditingId(null);
      } else {
        // Create new overlay
        await axios.post(API_URL, formData);
        alert('Overlay created successfully');
      }
      
      // Reset form and refresh list
      resetForm();
      fetchOverlays();
    } catch (error) {
      console.error('Error saving overlay:', error);
      alert('Failed to save overlay');
    }
  };

  const handleEdit = (overlay) => {
    setFormData({
      content: overlay.content,
      type: overlay.type,
      x: overlay.position.x,
      y: overlay.position.y,
      width: overlay.size.width,
      height: overlay.size.height
    });
    setEditingId(overlay.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this overlay?')) {
      try {
        await axios.delete(`${API_URL}/${id}`);
        alert('Overlay deleted successfully');
        fetchOverlays();
      } catch (error) {
        console.error('Error deleting overlay:', error);
        alert('Failed to delete overlay');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      content: '',
      type: 'text',
      x: 0,
      y: 0,
      width: 100,
      height: 50
    });
    setEditingId(null);
  };

  return (
    <div className="overlay-manager">
      <h2>Overlay Manager</h2>
      
      <form onSubmit={handleSubmit} className="overlay-form">
        <h3>{editingId ? 'Edit Overlay' : 'Create New Overlay'}</h3>
        
        <div className="form-group">
          <label>Content:</label>
          <input
            type="text"
            name="content"
            value={formData.content}
            onChange={handleInputChange}
            placeholder="Enter text or logo path"
            required
          />
        </div>

        <div className="form-group">
          <label>Type:</label>
          <select name="type" value={formData.type} onChange={handleInputChange}>
            <option value="text">Text</option>
            <option value="logo">Logo</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>X Position:</label>
            <input
              type="number"
              name="x"
              value={formData.x}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Y Position:</label>
            <input
              type="number"
              name="y"
              value={formData.y}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Width:</label>
            <input
              type="number"
              name="width"
              value={formData.width}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Height:</label>
            <input
              type="number"
              name="height"
              value={formData.height}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="button-group">
          <button type="submit" className="btn-submit">
            {editingId ? 'Update Overlay' : 'Create Overlay'}
          </button>
          {editingId && (
            <button type="button" onClick={resetForm} className="btn-cancel">
              Cancel Edit
            </button>
          )}
        </div>
      </form>

      <div className="overlay-list">
        <h3>Existing Overlays ({overlays.length})</h3>
        
        {loading ? (
          <p>Loading overlays...</p>
        ) : overlays.length === 0 ? (
          <p>No overlays created yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Content</th>
                <th>Type</th>
                <th>Position</th>
                <th>Size</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {overlays.map(overlay => (
                <tr key={overlay.id}>
                  <td>{overlay.content}</td>
                  <td>{overlay.type}</td>
                  <td>({overlay.position.x}, {overlay.position.y})</td>
                  <td>{overlay.size.width}x{overlay.size.height}</td>
                  <td>
                    <button onClick={() => handleEdit(overlay)} className="btn-edit">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(overlay.id)} className="btn-delete">
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default OverlayManager;

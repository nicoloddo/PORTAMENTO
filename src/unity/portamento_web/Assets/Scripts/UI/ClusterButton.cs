using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ClusterButton : MonoBehaviour
{
    public Cluster Cluster;
    public GameObject BackgroundHighlight;

    private float _x;
    private float _y;

    private float _xRange;
    private float _yRange;
    private string _xAxis;
    private string _yAxis;

    public Text Label;

    public void UpdatePosition()
    {
        RectTransform parentRect = transform.parent.GetComponent<RectTransform>();
        
        // Get parent dimensions
        float parentWidth = parentRect.rect.width;
        float parentHeight = parentRect.rect.height;
        Vector3 parentPos = parentRect.position;

        // Get the centroid coordinates
        float centroid_x = Cluster.Centroid[_xAxis];
        float centroid_y = Cluster.Centroid[_yAxis];

        // Pan them to -0.5 to 0.5
        centroid_x = (centroid_x - 0.5f);
        centroid_y = (centroid_y - 0.5f);
        
        // Calculate ranges based on parent dimensions
        _xRange = parentWidth*0.65f;
        _yRange = parentHeight*0.65f;
        
        // Calculate position relative to parent's position
        float parent_center_x = parentPos.x - (parentWidth/2);
        float parent_center_y = parentPos.y;

        // Add some padding due to the map image not fitting the entire parent
        parent_center_x += (parentWidth*0.1f); 
        parent_center_y += (parentHeight*0.1f);
        
        _x = parent_center_x + (centroid_x * _xRange);
        _y = parent_center_y + (centroid_y * _yRange);
        
        gameObject.GetComponent<RectTransform>().position = new Vector3(_x, _y, parentPos.z);
    }

    public void SetAxis(string horizontal, string vertical)
    {
        _xAxis = horizontal;
        _yAxis = vertical;  
    }

    public void SetNumber(string clusterNumber)
    {
        Label.text = clusterNumber;
    }

    public void Highlight()
    {
        BackgroundHighlight.SetActive(true);
    }

    public void Unselect()
    {
        BackgroundHighlight.SetActive(false);
    }
}

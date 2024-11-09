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

    public float XRangePercentage = 0.5f;
    public float YRangePercentage = 0.55f;

    public float ParentCenterXPaddingPercentage = 0.15f;
    public float ParentCenterYPaddingPercentage = 0f;

    public Text Label;

    public void Update()
    {
        //UpdatePosition(); Uncomment to debug the position in game
    }

    public void UpdatePosition()
    {
        RectTransform parentRect = transform.parent.GetComponent<RectTransform>();
        
        // Get parent dimensions
        float parentWidth = parentRect.rect.width;
        float parentHeight = parentRect.rect.height;
        Vector3 parentPos = parentRect.position;

        // Get the centroid coordinates
        float centroidX = Cluster.Centroid[_xAxis];
        float centroidY = Cluster.Centroid[_yAxis];

        // Pan them to -0.5 to 0.5
        centroidX = (centroidX - 0.5f);
        centroidY = (centroidY - 0.5f);
        
        // Calculate ranges based on parent dimensions
        _xRange = parentWidth*XRangePercentage;
        _yRange = parentHeight*YRangePercentage;
        
        // Calculate position relative to parent's position
        float parentCenterX = parentPos.x - (parentWidth/2);
        float parentCenterY = parentPos.y;

        // Add some padding due to the map image not fitting the entire parent
        parentCenterX += (parentWidth*ParentCenterXPaddingPercentage); 
        parentCenterY += (parentHeight*ParentCenterYPaddingPercentage);
        
        _x = parentCenterX + (centroidX * _xRange);
        _y = parentCenterY + (centroidY * _yRange);
        
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

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
    private string _xAxis;
    private string _yAxis;

    public Text Label;

    public void Update()
    {
        //UpdatePosition(); // Uncomment to debug the position in game
    }

    public void UpdatePosition()
    {        
        // Get parent dimensions
        RectTransform parentRect = transform.parent.GetComponent<RectTransform>();
        float parentWidth = parentRect.rect.width;
        float parentHeight = parentRect.rect.height;

        // Get the centroid coordinates
        float centroidX = Cluster.Centroid[_xAxis];
        float centroidY = Cluster.Centroid[_yAxis];
        // Pan them from 0 to 1 to -0.5 to 0.5
        centroidX -= 0.5f;
        centroidY -= 0.5f;

        // Calculate position relative to parent's size
        _x = centroidX * parentWidth;
        _y = centroidY * parentHeight;

        // Set the position
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        rectTransform.anchoredPosition = new Vector2(_x, _y);

        // Force Z position to 0 in local space
        Vector3 localPos = rectTransform.localPosition;
        localPos.z = 0;
        rectTransform.localPosition = localPos;

        // Set size as percentage of parent (e.g., 5%) accounting for Canvas scaling
        Canvas canvas = GetComponentInParent<Canvas>();
        float scaleFactor = canvas.scaleFactor;
        float sizePercentage = 0.05f;
        float size = parentRect.rect.width * sizePercentage * scaleFactor;
        rectTransform.sizeDelta = new Vector2(size, size);
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

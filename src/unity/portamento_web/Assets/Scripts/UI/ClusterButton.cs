using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ClusterButton : MonoBehaviour
{
    public Cluster Cluster;
    public GameObject BackgroundHighlight;

    public float XMin = -600;
    public float XMax = -150;

    public float YMin = 75;
    public float YMax = 525;

    private float _x;
    private float _y;

    private float _xRange;
    private float _yRange;
    private string _xAxis;
    private string _yAxis;

    public Text Label;

    public void UpdatePosition()
    {
        _xRange = XMax - XMin;
        _yRange = YMax - YMin;

        _x = XMin + Cluster.Centroid[_xAxis] * _xRange;
        _y = YMin + Cluster.Centroid[_yAxis] * _yRange;

        gameObject.GetComponent<RectTransform>().localPosition = new Vector3(_x + 50, _y - 315, 0);    // 50 and 315 are due to offset that were created in game
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

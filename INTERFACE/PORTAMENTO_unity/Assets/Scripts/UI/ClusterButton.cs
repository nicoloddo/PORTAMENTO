using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ClusterButton : MonoBehaviour
{
    public Cluster cluster;
    public GameObject background_highlight;

    public float x_min = -600;
    public float x_max = -150;

    public float y_min = 75;
    public float y_max = 525;

    public float x;
    public float y;

    private float x_range, y_range;
    private string x_axis, y_axis;

    public Text label;

    // Start is called before the first frame update
    void Start()
    {
        x_range = x_max - x_min;
        y_range = y_max - y_min;

        x = x_min + cluster.centroid[x_axis] * x_range;
        y = y_min + cluster.centroid[y_axis] * y_range;

        gameObject.GetComponent<RectTransform>().localPosition = new Vector3(x, y - 315, 0);    // Quel 315 è dovuto a un offset che si creava in game non so perchè
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void initialize(string orizontal, string vertical, string cluster_number)
    {
        x_axis = orizontal;
        y_axis = vertical;
        label.text = cluster_number;
    }

    public void highlight()
    {
        background_highlight.SetActive(true);
    }

    public void unselect()
    {
        background_highlight.SetActive(false);
    }
}

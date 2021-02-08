using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cluster : MonoBehaviour
{
    private List<Dictionary<string, float>> track = new List<Dictionary<string, float>>();
    private List<Dictionary<string, string>> meta = new List<Dictionary<string, string>>();

    public Dictionary<string, float> centroid = new Dictionary<string, float>();
    public bool is_leaf;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void set_is_leaf(bool is_leaf_bool)
    {
        is_leaf = is_leaf_bool;
    }

    public void set_centroid(Dictionary<string, float> centroid_params)
    {
        centroid = centroid_params;
    }

    public void set_cluster_data(List<Dictionary<string, float>> track_data, List<Dictionary<string, string>> meta_data)
    {
        track = track_data;
        meta = meta_data;
    }
}

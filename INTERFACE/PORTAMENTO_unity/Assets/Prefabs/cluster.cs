using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cluster : MonoBehaviour
{
    string id;
    private List<Dictionary<string, float>> track = new List<Dictionary<string, float>>();
    private List<Dictionary<string, string>> meta = new List<Dictionary<string, string>>();
    private string[] axis = new string[3];  // I nomi degli assi di riferimento (keys del dizionario delle caratteristiche track)
    int axis_multiplier = 100;

    public Dictionary<string, float> centroid = new Dictionary<string, float>();
    public bool is_leaf;

    // Start is called before the first frame update
    void Start()
    {
        transform.position = new Vector3(centroid[axis[0]] * axis_multiplier, centroid[axis[1]] * axis_multiplier, centroid[axis[2]] * axis_multiplier);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void set_id(string clust_id)
    {
        id = clust_id;
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

    public void set_axis(string x, string y, string z)
    {
        axis[0] = x;
        axis[1] = y;
        axis[2] = z;
    }

    public string get_id()
    {
        return id;
    }

}

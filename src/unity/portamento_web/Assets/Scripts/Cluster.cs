using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cluster : MonoBehaviour
{
    int axis_multiplier = 400; // Also present in SongMenu and DisplayMenu classes, used to space out clusters

    string id;
    public List<Dictionary<string, float>> track = new List<Dictionary<string, float>>();
    public List<Dictionary<string, string>> meta = new List<Dictionary<string, string>>();
    private string[] axis = new string[3];  // Names of the reference axes (keys of the track features dictionary)
    public Dictionary<string, float> centroid = new Dictionary<string, float>();
    public bool is_leaf;
    public bool player_near;

    private GameObject player;

    public GameObject highlight_supernova;
    public GameObject standard_supernova;

    // Start is called before the first frame update
    void Start()
    {
        transform.position = new Vector3(centroid[axis[0]] * axis_multiplier, centroid[axis[1]] * axis_multiplier, centroid[axis[2]] * axis_multiplier);
    }

    // Update is called once per frame
    void Update()
    {

    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.gameObject.CompareTag("Player"))
        {
            player_near = true;
            player = other.gameObject;
            player.GetComponent<PlayerController>().set_nearCluster(this.gameObject, player_near);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.CompareTag("Player"))
        {
            player_near = false;
            player = other.gameObject;
            player.GetComponent<PlayerController>().set_nearCluster(this.gameObject, player_near);
        }
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

    public void create_clusterButton(ClusterButton clust)
    {
        clust.cluster = this;
    }

    public void highlight()
    {
        highlight_supernova.SetActive(true);
        standard_supernova.SetActive(false);
    }

    public void unselect()
    {
        highlight_supernova.SetActive(false);
        standard_supernova.SetActive(true);
    }
}

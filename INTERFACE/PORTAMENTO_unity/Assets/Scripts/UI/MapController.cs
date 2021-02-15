using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MapController : MonoBehaviour
{
    List<GameObject> cluster_list = new List<GameObject>();
    List<GameObject> cluster_button_list = new List<GameObject>();
    public GameObject cluster_button_prefab;
    public GameObject radar_menu;
    public Text orizontal_label;
    public Text vertical_label;

    private List<Dictionary<string, float>> radar_track;
    private List<Dictionary<string, string>> radar_meta;

    private GameObject player;
    private GameObject selected_cluster;
    private GameObject selected_button;

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void append_cluster(GameObject cluster)
    {
        cluster_list.Add(cluster);
    }

    public void createMap(string x_axis, string y_axis)
    {
        orizontal_label.text = x_axis;
        vertical_label.text = y_axis;

        // CREO I PUNTI CLUSTER
        foreach(GameObject cluster in cluster_list)
        {
            GameObject cluster_button = Instantiate(cluster_button_prefab);
            cluster_button_list.Add(cluster_button);
            cluster_button.transform.SetParent(transform);   // Imposto il button cluster come figlio della mappa per controllarne bene il transform
            cluster.GetComponent<Cluster>().create_clusterButton(cluster_button.GetComponent<ClusterButton>());
            cluster_button.GetComponent<ClusterButton>().initialize(x_axis, y_axis, cluster.GetComponent<Cluster>().get_id());

            var button = cluster_button.GetComponent<Button>();
            button.onClick.AddListener(() => launch_button_clust(cluster_button, cluster));
        }

        radar_menu.GetComponent<RadarMenu>().CreateMenu(radar_meta, radar_track);
    }

    private void launch_button_clust(GameObject cluster_button, GameObject cluster)
    {
        if(selected_cluster != null)
        {
            selected_cluster.GetComponent<Cluster>().unselect();
            selected_button.GetComponent<ClusterButton>().unselect();
        }

        player.GetComponent<PlayerController>().setSelectedCluster(cluster.transform);
        selected_cluster = cluster;
        selected_button = cluster_button;
        cluster.GetComponent<Cluster>().highlight();
        cluster_button.GetComponent<ClusterButton>().highlight();
    }

    public void set_radars(List<Dictionary<string, float>> track_radars, List<Dictionary<string, string>> meta_radars)
    {
        radar_track = track_radars;
        radar_meta = meta_radars;
    }

    public void launch_button_from_index(int i)
    {
        launch_button_clust(cluster_button_list[i], cluster_list[i]);
    }

}

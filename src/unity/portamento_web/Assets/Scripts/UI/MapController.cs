using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MapController : MonoBehaviour
{
    private List<string> _axis = new List<string>();
    private int _x = 0;
    private int _y = 1;

    private List<GameObject> _clusterList = new List<GameObject>();
    private List<GameObject> _clusterButtonList = new List<GameObject>();
    public GameObject ClusterButtonPrefab;
    public GameObject RadarMenu;
    public Text HorizontalLabel;
    public Text VerticalLabel;

    private List<Dictionary<string, float>> _radarTrack;
    private List<Dictionary<string, string>> _radarMeta;

    private GameObject _player;
    private GameObject _selectedCluster;
    private GameObject _selectedButton;

    void Start()
    {
        _player = GameObject.FindGameObjectWithTag("Player");
    }

    public void AppendCluster(GameObject cluster)
    {
        _clusterList.Add(cluster);
    }

    public void AppendAxis(string attribute)
    {
        _axis.Add(attribute);
    }

    public void SetX(int i)
    {
        _x = i;
    }

    public void SetY(int i)
    {
        _y = i;
    }

    public void IncrementX(int increment)
    {
        _x += increment;
        if(_x >= _axis.Count)     // To handle the rotation of the values through the list index
        {
            _x = 0;
        }
        else if (_x <= -1)
        {
            _x = _axis.Count - 1;
        }

        foreach (GameObject clusterButton in _clusterButtonList)
        {
            clusterButton.GetComponent<ClusterButton>().SetAxis(_axis[_x], _axis[_y]);
            clusterButton.GetComponent<ClusterButton>().UpdatePosition();
        }
        HorizontalLabel.text = _axis[_x];
    }

    public void IncrementY(int increment)
    {
        _y += increment;
        if (_y >= _axis.Count)    // To handle the rotation of the values through the list index
        {
            _y = 0;
        }
        else if (_y <= -1)
        {
            _y = _axis.Count - 1;
        }

        foreach (GameObject clusterButton in _clusterButtonList)
        {
            clusterButton.GetComponent<ClusterButton>().SetAxis(_axis[_x], _axis[_y]);
            clusterButton.GetComponent<ClusterButton>().UpdatePosition();
        }
        VerticalLabel.text = _axis[_y];
    }

    public void CreateMap()
    {
        HorizontalLabel.text = _axis[_x];
        VerticalLabel.text = _axis[_y];

        foreach(GameObject cluster in _clusterList)
        {
            GameObject clusterButton = Instantiate(ClusterButtonPrefab);
            _clusterButtonList.Add(clusterButton);
            clusterButton.transform.SetParent(transform);   // Set the cluster button as a child of the map to easily control its transform
            cluster.GetComponent<Cluster>().CreateClusterButton(clusterButton.GetComponent<ClusterButton>());
            clusterButton.GetComponent<ClusterButton>().SetAxis(_axis[_x], _axis[_y]);
            clusterButton.GetComponent<ClusterButton>().SetNumber(cluster.GetComponent<Cluster>().GetId());
            clusterButton.GetComponent<ClusterButton>().UpdatePosition();

            var button = clusterButton.GetComponent<Button>();
            button.onClick.AddListener(() => SelectCluster(clusterButton, cluster));
        }

        RadarMenu.GetComponent<RadarMenu>().CreateMenu(_radarMeta, _radarTrack);
    }

    private void SelectCluster(GameObject clusterButton, GameObject cluster)
    {
        if(_selectedCluster != null)
        {
            _selectedCluster.GetComponent<Cluster>().Unselect();
            _selectedButton.GetComponent<ClusterButton>().Unselect();
        }

        _player.GetComponent<PlayerController>().SetSelectedCluster(cluster.transform);
        _selectedCluster = cluster;
        _selectedButton = clusterButton;
        cluster.GetComponent<Cluster>().Highlight();
        clusterButton.GetComponent<ClusterButton>().Highlight();

        _player.GetComponent<PlayerController>().GetGameManager().StatusLabel.SetStatus("Press E in-game\n to point at the selected mini-universe");
    }

    public void SetRadars(List<Dictionary<string, float>> radarTrack, List<Dictionary<string, string>> radarMeta)
    {
        _radarTrack = radarTrack;
        _radarMeta = radarMeta;
    }

    public void SelectClusterFromIndex(int i)
    {
        SelectCluster(_clusterButtonList[i], _clusterList[i]);
    }
}

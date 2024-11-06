using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cluster : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400; // Also present in SongMenu and DisplayMenu classes, used to space out clusters

    private string _id;
    public List<Dictionary<string, float>> Track = new List<Dictionary<string, float>>();
    public List<Dictionary<string, string>> Meta = new List<Dictionary<string, string>>();
    private string[] _axis = new string[3];  // Names of the reference axes (keys of the track features dictionary)
    public Dictionary<string, float> Centroid = new Dictionary<string, float>();
    private bool _isLeaf;
    private bool _playerNear;

    private GameObject _player;

    public GameObject HighlightSupernova;
    public GameObject StandardSupernova;

    // Start is called before the first frame update
    void Start()
    {
        transform.position = new Vector3(
            Centroid[_axis[0]] * AXIS_MULTIPLIER, 
            Centroid[_axis[1]] * AXIS_MULTIPLIER, 
            Centroid[_axis[2]] * AXIS_MULTIPLIER
        );
    }

    // Update is called once per frame
    void Update()
    {

    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.gameObject.CompareTag("Player"))
        {
            _playerNear = true;
            _player = other.gameObject;
            _player.GetComponent<PlayerController>().SetNearCluster(this.gameObject, _playerNear);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.CompareTag("Player"))
        {
            _playerNear = false;
            _player = other.gameObject;
            _player.GetComponent<PlayerController>().SetNearCluster(this.gameObject, _playerNear);
        }
    }

    public void SetId(string clustId)
    {
        _id = clustId;
    }

    public void SetIsLeaf(bool isLeafBool)
    {
        _isLeaf = isLeafBool;
    }

    public void SetCentroid(Dictionary<string, float> centroidParams)
    {
        Centroid = centroidParams;
    }

    public void SetClusterData(List<Dictionary<string, float>> trackData, List<Dictionary<string, string>> metaData)
    {
        Track = trackData;
        Meta = metaData;
    }

    public void SetAxis(string x, string y, string z)
    {
        _axis[0] = x;
        _axis[1] = y;
        _axis[2] = z;
    }

    public string GetId()
    {
        return _id;
    }

    public void CreateClusterButton(ClusterButton clust)
    {
        clust.Cluster = this;
    }

    public void Highlight()
    {
        HighlightSupernova.SetActive(true);
        StandardSupernova.SetActive(false);
    }

    public void Unselect()
    {
        HighlightSupernova.SetActive(false);
        StandardSupernova.SetActive(true);
    }

    public bool IsLeaf
    {
        get { return _isLeaf; }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400; // Also present in SongMenu, DisplayMenu and Cluster classes: used to space out clusters

    // USEFUL ASSIGNMENTS
    private Animator _animator;
    private CharacterController _characterController;
    public Vector3 LookatRotation { get; private set; }

    // INPUT DELAY
    private float _justPressed = 0; // Used to wait before receiving a new input. Prevents immediate menu closure if pressed slightly too long
    private const float JUST_PRESSED_MAX = 0.1f;

    // REFERENCES
    public new GameObject camera;
    private GameManager _gameManager;
    private GameObject _nearCluster;

    // STATE FLAGS
    private bool _firstRun = true;
    private bool _isNear = false;
    private bool _canMove = true;
    private bool _songMenuOpened = false;
    private bool _mapOpened = false;

    // INPUT VARIABLES
    private float _inputUpward; // For upward movement
    private float _inputVertical; // Keys for forward movement
    private float _inputHorizontal; // Keys for rotation (in addition to mouse)
    public float TotalXRotation { get; private set; } // Total X rotation
    public float TotalYRotation { get; private set; } // Total Y rotation

    // MOVEMENT PARAMETERS
    private const float ROTATE_SPEED_X = 4f; // X rotation speed
    private const float ROTATE_SPEED_Y = 3f; // Y rotation speed
    public float ForwardSpeed = 0.8f; // Forward movement speed
    public float LateralSpeed = 0.5f; // Lateral movement speed
    public float UpwardSpeed = 0.5f; // Upward movement speed

    // NAVIGATION
    public string CurrentClusterId;
    public Transform SelectedClusterTransform;

    private void Awake()
    {
        CurrentClusterId = PlayerPrefs.GetString("current_node_id", "0");
        _gameManager = FindObjectOfType<GameManager>();
        _animator = GetComponent<Animator>();
        _characterController = GetComponent<CharacterController>();
    }

    private void Update()
    {
        if (!_gameManager.FetchedNodeData)
            return;

        if(_justPressed < JUST_PRESSED_MAX + 5)
            _justPressed += Time.deltaTime;

        if (_firstRun)
        {
            // Disable and re-enable the character controller to allow teleportation
            _characterController.enabled = false;
            transform.position = GetStartPosition();
            _firstRun = false;
            _characterController.enabled = true;
        }

        if (Input.GetKey("f") && _isNear && !_mapOpened && _justPressed > JUST_PRESSED_MAX)
        {
            if(!_songMenuOpened)
            {
                SongMenuRun();
                _animator.SetFloat("fly", 0);    // Stop the player
                _justPressed = 0;   // Start the timer
            }
            else if(_justPressed > 1)
            {
                SongMenuEsc();
                _justPressed = 0;   // Start the timer
            }  
        }

        if (Input.GetKey("m") && !_songMenuOpened && _justPressed > JUST_PRESSED_MAX)
        {
            if (!_mapOpened)
            {
                MapShow();
                _animator.SetFloat("fly", 0);    // Stop the player
                _justPressed = 0;   // Start the timer
            }
            else if (_justPressed > 1)
            {
                MapEsc();
                _justPressed = 0;   // Start the timer
            }
        }

        if (Input.GetKey("r") && !_songMenuOpened && !_mapOpened)
        {
            transform.LookAt(SelectedClusterTransform);
            TotalXRotation = transform.rotation.eulerAngles.y;
            TotalYRotation = transform.rotation.eulerAngles.x;
        }

        if (Input.GetKey("z") && !_songMenuOpened && !_mapOpened)
        {
            TotalYRotation = 0;
        }

        if (Input.GetKey("x") && !_songMenuOpened && !_mapOpened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                TotalXRotation = 90;
                TotalYRotation = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                TotalXRotation = -90;
                TotalYRotation = 0;
            }
        }

        if (Input.GetKey("c") && !_songMenuOpened && !_mapOpened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                TotalXRotation = 0;
                TotalYRotation = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                TotalXRotation = 180;
                TotalYRotation = 0;
            }
        }
    }

    private void FixedUpdate()
    {
        if (!_gameManager.FetchedNodeData)
            return;

        // Movement management
        if (_canMove)
        {
            _inputVertical = Input.GetAxis("Vertical");
            _inputHorizontal = Input.GetAxis("Horizontal");
            _inputUpward = Input.GetAxis("Jump");

            _animator.SetFloat("fly", _inputVertical);

            // Rotation controller, designed to avoid z-axis rotation that can occur from summing x and y rotations
            TotalXRotation += Input.GetAxis("Mouse X") * ROTATE_SPEED_X;
            TotalYRotation -= Input.GetAxis("Mouse Y") * ROTATE_SPEED_Y;

            transform.forward = camera.transform.forward;

            if (_inputVertical > 0)
            {
                camera.transform.rotation = Quaternion.Euler(TotalYRotation, TotalXRotation, 0f);
            }
            else
            {
                camera.transform.rotation = transform.rotation;
                transform.rotation = Quaternion.Euler(0f, TotalXRotation, 0f);
                camera.transform.rotation = Quaternion.Euler(TotalYRotation, TotalXRotation, 0f);
            }

            // Movement
            _characterController.Move(camera.transform.forward * _inputVertical * ForwardSpeed);
            _characterController.Move(camera.transform.right * _inputHorizontal * ForwardSpeed);
            _characterController.Move(camera.transform.up * _inputUpward * UpwardSpeed);
        }
    }

    private void MapShow()
    {
        _mapOpened = true;
        _canMove = false;
        _gameManager.ViewMap();
    }

    private void MapEsc()
    {
        _mapOpened = false;
        _canMove = true;
        _gameManager.CloseMap();
    }

    private string SongMenuRun()
    {
        _songMenuOpened = true;
        _canMove = false;
        return _gameManager.StartSongMenu(_nearCluster);
    }

    private void SongMenuEsc()
    {
        _songMenuOpened = false;
        _canMove = true;
        _gameManager.StopSongMenu();
    }

    public void SetNearCluster(GameObject cluster, bool isNear)
    {
        _nearCluster = cluster;
        _isNear = isNear;
    }

    public void EnterCluster(string clusterId, bool isLeaf)
    {
        if (!isLeaf) 
        {
            CurrentClusterId = CurrentClusterId + clusterId;   // Update the CurrentClusterId, which is kept within the player.
            PlayerPrefs.SetString("current_node_id", CurrentClusterId);
            Invoke(nameof(LoadScene), 0);
        }
        else 
        {
            _gameManager.StatusLabel.SetStatus("This universe is too small for you to enter!");
            Debug.Log("The cluster is a leaf cluster!");
        }
    }

    public void SetSelectedCluster(Transform selected)
    {
        SelectedClusterTransform = selected;
    }

    public Vector3 GetStartPosition()
    {
        Dictionary<string, string> axis = _gameManager.Axis;
        Dictionary<string, float> centroid = _gameManager.FirstCentroid;
        return new Vector3(
            centroid[axis["x"]] * AXIS_MULTIPLIER + 2, 
            centroid[axis["y"]] * AXIS_MULTIPLIER,
            centroid[axis["z"]] * AXIS_MULTIPLIER
        );
    }

    private void OnApplicationQuit()
    {
        PlayerPrefs.DeleteAll();
    }

    private void LoadScene()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}

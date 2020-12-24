using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    Rigidbody rb;
    public float forceMult = 1;
    bool isGrounded;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        isGrounded = false;
    }

    // Update is called once per frame
    void Update()
    {

    }


    private void FixedUpdate()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");



        if (isGrounded)
        {
            float jump = Input.GetAxis("Jump");
            Vector3 jumpForce = new Vector3(0f, jump * forceMult, 0f);
            rb.AddForce(jumpForce, ForceMode.Impulse);

        }

        Vector3 movement = new Vector3(horizontal * forceMult, 0.0f, vertical * forceMult);

        rb.AddForce(movement);

    }

    private void OnCollisionEnter(Collision collision)
    {
        isGrounded = false;
    }

    private void OnCollisionExit(Collision collision)
    {
        isGrounded = false;
    }



}

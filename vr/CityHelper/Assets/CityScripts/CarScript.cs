using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarScript : MonoBehaviour {

    bool isWaiting = false;
    bool isFirst = false;
    public string direction;

    bool isCarInFront()
    {
        foreach (GameObject gobj in GameManager.instance.spawnedCars)
        {
            if (gobj == gameObject)
                continue;

            if (gobj.GetComponent<CarScript>().direction == gameObject.GetComponent<CarScript>().direction)
               
            {
                float value = 100000000f;
                if (gobj.GetComponent<CarScript>().direction[0] == 'x' && Mathf.Abs(gobj.transform.position.z - gameObject.transform.position.z) < 5)
                {
                    value = gobj.transform.position.x - gameObject.transform.position.x;
                }
                else if (gobj.GetComponent<CarScript>().direction[0] == 'z' && Mathf.Abs(gobj.transform.position.x - gameObject.transform.position.x) < 5)
                {
                    value = gobj.transform.position.z - gameObject.transform.position.z;
                }
                if (gobj.GetComponent<CarScript>().direction[1] == '-')
                {
                    value = -value;
                }
                if (value > 0 && value < 30f)
                {
                    return true;
                }
            }
        }
        return false;
    }

    void FixedUpdate()
    {
        if (isWaiting)
        {
            if (!isCarInFront())
            {
                launchCar(false);
                return;
            }
        }
        else
        {
            if (isCarInFront())
            {
                stopCar(false);
                return;
            }
        }
        
    }

    public void stopCar(bool first)
    {
        if (first)
        {
            isFirst = true;
        }
        else
        {
            if (isFirst)
            {
                return;
            }
            isWaiting = true;
        }
        gameObject.GetComponent<Rigidbody>().velocity = Vector3.zero;
    }

    public void launchCar(bool first)
    {
        if (first)
        {
            isFirst = false;
        }
        else
        {
            if (isFirst)
            {
                return;
            }
            isWaiting = false;
        }
        Vector3 startForce = GameManager.instance.GetForceVectorForDirection(direction);
        gameObject.GetComponent<Rigidbody>().AddForce(startForce);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IntersectionScript : MonoBehaviour {

    public GameObject trigger1;
    public GameObject trigger2;
    public GameObject trigger3;
    public GameObject trigger4;

    public int greenSeconds;
    public int cooldownSeconds;

    private int framesLeft;

    private bool areAnyAllowed;
    private bool wasTrigger1Last;

    // Use this for initialization
    void Start() {
        areAnyAllowed = false;
        wasTrigger1Last = false;
        framesLeft = 0;
    }

    // Update is called once per frame
    void Update() {
        if (framesLeft > 0)
        {
            framesLeft--;
        }
        else
        {
            Switch();
        }
    }

    public void Switch() {
        Debug.Log("switching " + wasTrigger1Last + " " + areAnyAllowed);
        if (!areAnyAllowed)
        {
            if (!wasTrigger1Last)
            {
                trigger1.GetComponent<TriggerScript>().stopCars = false;
                trigger2.GetComponent<TriggerScript>().stopCars = false;
                wasTrigger1Last = true;
                areAnyAllowed = true;
                framesLeft = (int) (greenSeconds * 1 / Time.deltaTime);
            }
            else
            {
                trigger3.GetComponent<TriggerScript>().stopCars = false;
                trigger4.GetComponent<TriggerScript>().stopCars = false;
                areAnyAllowed = true;
                wasTrigger1Last = false;
                framesLeft = (int)(greenSeconds * 1 / Time.deltaTime);
            }
        }
        else
        {
            if (!wasTrigger1Last)
            {
                trigger3.GetComponent<TriggerScript>().stopCars = true;
                trigger4.GetComponent<TriggerScript>().stopCars = true;
                areAnyAllowed = false;
                wasTrigger1Last = false;
                framesLeft = (int)(cooldownSeconds * 1 / Time.deltaTime);
            }
            else
            {
                trigger1.GetComponent<TriggerScript>().stopCars = true;
                trigger2.GetComponent<TriggerScript>().stopCars = true;
                areAnyAllowed = false;
                wasTrigger1Last = true;
                framesLeft = (int)(cooldownSeconds * 1 / Time.deltaTime);
            }
        }
    }
}

import streamlit as st

def main():
    st.title("BMI calculator")

    # """
    # ## Note: ##
    # ---------------------
    # **This is a bmi calculator**\n
    # ---------------------
    # """

    css="""
    <style>
        .button-pri {
            background: LightBlue;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)
    
    status = st.selectbox("height:",["meters","foot"])
    if status == "meters":
        height = float(st.text_input("height in meters","100",None,"height"))
    else:
        height = int(st.text_input("height in foot", "5", None, "height"))
        inches = int(st.text_input("inches", "0", None, "inches"))
        height = 0.0254*((height*12)+inches)

    status = st.selectbox("weight:", ["kilogram", "pound"])

    weight = float(st.text_input("weight", "100", None))
    
    if status == "pound":
        weight = 0.453592*weight

    if st.button("Calculate", type="primary", key='buttonpri'):
            st.markdown((weight/height)**2)
    

main()
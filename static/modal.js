class Modal{
    element = null;
    constructor(element) {
        this.element_name = element;
        this.element = this.getElement();
    }

    getElement(){
        if(this.element_name.startsWith("#")){
            return document.getElementById(this.element_name);
        } else {
            if(this.element_name.startsWith(".")){
                return (document.getElementsByClassName(this.element_name).length > 0) ? document.getElementsByClassName(this.element_name)[0] : null;
            } else {
                return (document.getElementsByName(this.element_name).length > 0) ? document.getElementsByName(this.element_name)[0] : null;
            }
        }
    }

    changeModalState(){
        if(this.element != null){
            if(this.element.classList.contains("active")){
                this.element.classList.remove("active");
            } else {
                this.element.classList.add("active");
            }
        }
    }

}
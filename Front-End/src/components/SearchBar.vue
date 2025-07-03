<template>
    <div class="rectangle">
        <div class="rectangle-content">
            <div class="start-end">
                <p>From</p>
            </div>
            <div class="icon-input-container">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M20 10.0001C20 14.9931 14.461 20.1931 12.601 21.7991C12.4277 21.9294 12.2168 21.9998 12 21.9998C11.7832 21.9998 11.5723 21.9294 11.399 21.7991C9.539 20.1931 4 14.9931 4 10.0001C4 7.87833 4.84285 5.8435 6.34315 4.34321C7.84344 2.84292 9.87827 2.00006 12 2.00006C14.1217 2.00006 16.1566 2.84292 17.6569 4.34321C19.1571 5.8435 20 7.87833 20 10.0001Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 13.0001C13.6569 13.0001 15 11.6569 15 10.0001C15 8.34321 13.6569 7.00006 12 7.00006C10.3431 7.00006 9 8.34321 9 10.0001C9 11.6569 10.3431 13.0001 12 13.0001Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="input-zone"> 
                    <input type="text" class="input">
                </div>
            </div>
            <div class="bullet-point-container">
                <div class="bullet-point"></div>
                <div class="bullet-point"></div>
                <div class="bullet-point"></div>
            </div>
            <div class="start-end">
                <p>To</p>
            </div>
            <div class="icon-input-container">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 16L16 12L12 8" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M8 12H16" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="input-zone"> 
                    <input type="text" class="input">
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

</script>

<style scoped>
.rectangle {
    background-color: white;
    width: 555px;
    height: 220px;
    border-radius: 25px;
    border: 2px solid #000;
    display: flex;
    flex-direction: column;
}

.start-end {
    font-family: 'Open Sans';
    font-weight: 700;
    color: #DDD;
    margin-top: -30px
}

.rectangle-content {
    margin-left: 14px;
}

.icon-input-container {
    display: flex;
    flex-direction: row;
    margin-top: -53px;
}

.input {
    border-top: none;
    border-left: none;
    border-right: none;
    outline: none;
    border-color: #BFBFBF;;
    padding-bottom: 5px;
    width: 265px;
    font-size: 20px;
}

.input-zone {
    margin-left: 10px;
}

.input:focus {
    border-bottom-color: black;
}

.bullet-point {
    width: 6px;
    height: 6.412px;
    background-color: black;
    border-radius: 50%;
}

.bullet-point-container {
    margin-top: -10px;
    margin-left: 9px;
    height: 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
</style>
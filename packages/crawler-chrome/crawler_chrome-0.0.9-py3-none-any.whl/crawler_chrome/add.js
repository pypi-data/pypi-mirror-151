function find_elements_xpath(xpath) {
    let result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
    let nodes = result.iterateNext(); //枚举第一个元素
    let res = [nodes];
    while (nodes) {
        nodes = result.iterateNext();
        res.push(nodes);
    }
    return res;
}
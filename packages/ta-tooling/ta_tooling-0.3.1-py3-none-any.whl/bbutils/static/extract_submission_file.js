/* Select the ul element containing the list of submision.
 *
 * The compiled version of this script is meant to be injected into correct iframe
 * of Blackboard.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var _a, _b;
function postData(url = "", data = {}) {
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield fetch(url, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
            },
            redirect: "manual",
            referrerPolicy: "no-referrer",
            body: JSON.stringify(data),
        });
        return response.json();
    });
}
let target_ul = document.querySelector("#pageList");
if (target_ul !== null) {
    let submission_list = target_ul.children || new HTMLCollection();
    let results = new Array();
    for (let i = 0; i < submission_list.length; i++) {
        let entry;
        let name;
        let url;
        let name_element = ((_a = submission_list.item(i)) === null || _a === void 0 ? void 0 : _a.querySelector("div.item h3")) || new HTMLElement();
        let file_element = (_b = submission_list === null || submission_list === void 0 ? void 0 : submission_list.item(i)) === null || _b === void 0 ? void 0 : _b.querySelector("div.details td#meta_value_2 a");
        name = name_element.textContent || "";
        if (file_element !== null && file_element !== undefined) {
            url = file_element.href || "";
        }
        else {
            url = "";
        }
        results.push({ name: name, url: url });
    }
    postData("http://localhost:5000/", { submission_files: results });
}

import pytest
from src.main import get_website_name_from_url
from src.main import get_product_price_from_url
from src.main import convert_price_tag_to_string

# Tests for get_website_name_from_url function
def test_get_best_buy_from_url():
    assert get_website_name_from_url("https://www.bestbuy.com/site/asus-rog-zephyrus-g14-14-oled-3k-120hz-gaming-laptop-amd-ryzen-9-8945hs-16gb-lpddr5x-nvidia-geforce-rtx-4060-1tb-ssd-platinum-white/6570270.p?skuId=6570270") == "BestBuy"
    
def test_get_target_from_url():
    assert get_website_name_from_url("https://www.target.com/p/apple-watch-series-10-aluminum-case-2024/-/A-93598395?preselect=91122628#lnk=sametab") == "Target"
    
def test_get_walmart_from_url():
    assert get_website_name_from_url("https://www.walmart.com/ip/iBUYPOWER-Slate-6-Mesh-Gaming-Desktop-Intel-i5-13600KF-NVIDIA-GeForce-RTX-4060-16GB-DDR5-1TB-NVMe-SSD-Liquid-Cooled-RGB-Windows-11-Home-64-bit-SlateM/5001803453") == "Walmart"
    
def test_get_amazon_from_url():
    assert get_website_name_from_url("https://www.amazon.com/CyberPowerPC-i5-13400F-GeForce-Windows-GXiVR8060A24/dp/B0DCMPRRFD/ref=asc_df_B0DCMPRRFD?mcid=4b6eb29325c138bca30ca43035efd8ba&hvocijid=15788773264263093910-B0DCMPRRFD-&hvexpln=73&tag=hyprod-20&linkCode=df0&hvadid=721245378154&hvpos=&hvnetw=g&hvrand=15788773264263093910&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9032154&hvtargid=pla-2281435179978&th=1") == "Amazon"
    
def test_unknown_website_from_url():
    website_url = "https://github.com/ridgethebridge/pEYEthon"
    
    with pytest.raises(ValueError) as exc_info:
        get_website_name_from_url(website_url)
    assert str(exc_info.value) == f"Invalid Website URL: {website_url}"
    
def test_get_best_buy_product_price_from_url():
    assert get_product_price_from_url("https://www.bestbuy.com/site/asus-rog-zephyrus-g14-14-oled-3k-120hz-gaming-laptop-amd-ryzen-9-8945hs-16gb-lpddr5x-nvidia-geforce-rtx-4060-1tb-ssd-platinum-white/6570270.p?skuId=6570270") == 1599.99
    
# Tests for helper functions
def test_convert_price_tag_to_string():
    assert convert_price_tag_to_string("$1,599.99") == 1599.99
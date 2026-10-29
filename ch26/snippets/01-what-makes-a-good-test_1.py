# the shape of a test; Cart and Item stand for your own classes
def test_discount_is_capped_at_50_percent():
    cart = Cart(items=[Item("Laptop", 45000)], coupon="MEGA90")     # arrange
    total = cart.total()                                           # act
    assert total == 22500                                          # assert

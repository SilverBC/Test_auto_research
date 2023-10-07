import org.junit.After;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.interactions.Actions;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class CommerceTest {
    final String USERNAME = "standard_user";
    final String LOCKEDUSERNAME = "locked_out_user";
    final String GLITCHUSERNAME = "performance_glitch_user";
	final String PASSWORD = "secret_sauce";

    private WebDriver driver;
    private Wait<WebDriver> wait;
    private Actions actions;

    public void setUp(String url) {
	    Dimension dimension = new Dimension(1920, 1080);
        ChromeOptions options = new ChromeOptions();
        //options.addArguments("--headless=new");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(4));
        driver.manage().window().setSize(dimension);
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.get(url);

        actions = new Actions(driver);
    }

    public void logIn(String name, String password) {
        driver.findElement(By.id("user-name")).sendKeys(name);
        driver.findElement(By.id("password")).sendKeys(password);
        driver.findElement(By.id("login-button")).click();

        List<WebElement> elements = driver.findElements(By.id("inventory_container"));
        assertTrue(elements.size() > 0);
    }

    public void logOut(){
        driver.findElement(By.id("react-burger-menu-btn")).click();
        driver.findElement(By.id("logout_sidebar_link")).click();
        
        List<WebElement> elements = driver.findElements(By.className("login_container"));
        assertTrue(elements.size() > 0);
    }

    @After
    public void teardown() {
        logOut();
        driver.quit();
    }

    @Test
    public void test() {
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
        driver.findElement(By.id("shopping_cart_container")).click();

        WebElement cartPageElement = driver.findElement(By.className("cart_list"));
        wait.until(d -> cartPageElement.isDisplayed());

	    String cartItemName = driver.findElement(By.className("inventory_item_name")).getText();
	    assertEquals(cartItemName, "Sauce Labs Backpack");

	    driver.findElement(By.id("checkout")).click();
	    WebElement checkoutPageElement = driver.findElement(By.id("checkout_info_container"));
	    wait.until(d -> checkoutPageElement.isDisplayed());

        driver.findElement(By.id("first-name")).sendKeys("John");
        driver.findElement(By.id("last-name")).sendKeys("Doe");
        driver.findElement(By.id("postal-code")).sendKeys("10001");
        driver.findElement(By.id("continue")).click();

        String checkoutItemName = driver.findElement(By.className("inventory_item_name")).getText();
        assertEquals(checkoutItemName, "Sauce Labs Backpack");

        driver.findElement(By.id("finish")).click();

        boolean successIsDisplayed = driver.findElement(By.id("checkout_complete_container")).isDisplayed();
        assertTrue(successIsDisplayed);
    }

    @Test
    public void assert_item_name_on_item_info_page(){
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        //go to the item
        driver.findElement(By.id("item_4_title_link")).click();

        //Check that texts exist on the site 
        // Sauce Labs Backpack
        assertEquals("Sauce Labs Backpack", driver.findElement(By.className("inventory_details_name")).getText());
        String expected = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.";
        assertEquals(expected, driver.findElement(By.className("inventory_details_desc")).getText());
    }


    @Test
    public void Move_To_LinkedIn(){
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        //Scroll down
        actions.moveToElement(driver.findElement(By.className("social_linkedin")));
        //Go to Linkedin page
        driver.findElement(By.className("social_linkedin")).click();;

        //Verify you are on the Linkedin page
        List<String> tabList = new ArrayList<>(driver.getWindowHandles());
        driver.switchTo().window(tabList.get(1)); 

        assertEquals("https://www.linkedin.com/company/sauce-labs/", driver.getCurrentUrl());
        driver.close();
        driver.switchTo().window(tabList.get(0));
    }

    @Test
    public void Assert_Sorting(){
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        //Click the filters box
        driver.findElement(By.className("select_container")).click();
        //click Z-A
        driver.findElement(By.cssSelector("option[value='za']")).click();
        //check that the name at the top is "Test.allTheThings() T-Shirt (Red)
        assertEquals("Test.allTheThings() T-Shirt (Red)", driver.findElement(By.cssSelector(".inventory_item_name")).getText());

        //click the filters box
        driver.findElement(By.className("select_container")).click();
        //click A-Z 
        driver.findElement(By.cssSelector("option[value='az']")).click();
        //check that the name at the top is "Sauce Labs Backpack"
        assertEquals("Sauce Labs Backpack", driver.findElement(By.cssSelector(".inventory_item_name")).getText());

        //click the filters box
        driver.findElement(By.className("select_container")).click();
        //click low-High
        driver.findElement(By.cssSelector("option[value='hilo']")).click();
        //check that the name at the top is "Sauce Labs Onesie"
        assertEquals("Sauce Labs Fleece Jacket", driver.findElement(By.cssSelector(".inventory_item_name")).getText());

        //click the filters box
        driver.findElement(By.className("select_container")).click();
        //click high-Low
        driver.findElement(By.cssSelector("option[value='lohi']")).click();
        //check that the name at the top is "Sauce Labs Fleece Jacket"
        assertEquals("Sauce Labs Onesie", driver.findElement(By.cssSelector(".inventory_item_name")).getText());
    }


    @Test
    public void Assert_Shopping_Button_States(){
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        driver.findElements(By.cssSelector("[id^=add-to-cart]")).forEach(button -> {
            actions.moveToElement(button).perform();
            button.click();
        });

        //check that the cart button says 6
        assertEquals("6", driver.findElement(By.className("shopping_cart_badge")).getText());

        driver.findElements(By.cssSelector("[id^=remove]")).forEach(button -> {
            actions.moveToElement(button).perform();
            button.click();
        }); 
       
        //check that the cart button says nothing
        assertTrue(driver.findElements(By.className("shopping_cart_badge")).size() < 1);
    }

    @Test
    public void Assert_User_Log_In_Cache_Permanency(){
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);
        //Add items to cart
        actions.moveToElement(driver.findElement(By.id("add-to-cart-sauce-labs-backpack")));
        driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
        actions.moveToElement(driver.findElement(By.id("add-to-cart-sauce-labs-bike-light")));
        driver.findElement(By.id("add-to-cart-sauce-labs-bike-light")).click();

        logOut();
        //check that items are still in the cart
        logIn(USERNAME, PASSWORD);

        assertEquals("2", driver.findElement(By.className("shopping_cart_badge")).getText());
    }

    @Test
    public void Assert_App_Reset_Functionality(){   //flaky test
        setUp("https://www.saucedemo.com");
        logIn(USERNAME, PASSWORD);

        //select all items
        driver.findElements(By.cssSelector("[id^=add-to-cart]")).forEach(button -> {
            actions.moveToElement(button).perform();
            button.click();
        });

        //click on sidebar
        driver.findElement(By.id("react-burger-menu-btn")).click();
        //click on Reset App State
        driver.findElement(By.id("reset_sidebar_link")).click();
        driver.findElement(By.id("react-burger-cross-btn")).click();
        //check that the app reset but that there is a bug with "Remove" still staying instead of resetting to Add Cart
        assertTrue(driver.findElements(By.className("shopping_cart_badge")).size() < 1);

        assertTrue(driver.findElement(By.id("remove-sauce-labs-backpack")).isDisplayed());
        assertTrue(driver.findElement(By.id("remove-sauce-labs-bike-light")).isDisplayed());
        assertTrue(driver.findElement(By.id("remove-sauce-labs-bolt-t-shirt")).isDisplayed());
        assertTrue(driver.findElement(By.id("remove-sauce-labs-fleece-jacket")).isDisplayed());
        assertTrue(driver.findElement(By.id("remove-sauce-labs-onesie")).isDisplayed());
        assertTrue(driver.findElement(By.id("remove-test.allthethings()-t-shirt-(red)")).isDisplayed());

        driver.findElement(By.id("react-burger-cross-btn")).click();
    }

    @Test
    public void Assert_Error_Accessing_Without_Log_In(){
        setUp("https://www.saucedemo.com/cart.html");  //write the direct link here
        //assert that the error is the correct one
        String expected = "Epic sadface: You can only access '/cart.html' when you are logged in.";
        assertEquals(expected, driver.findElement(By.className("error-message-container")).getText());

        logIn(USERNAME, PASSWORD);

        //now try logging in and then jumping to a link
        driver.get("https://www.saucedemo.com/cart.html");

        //assert that it worked when you were logged in
        assertTrue(driver.findElement(By.id("cart_contents_container")).isDisplayed());
    }

    @Test
    public void Assert_Locked_Out_User(){
        setUp("https://www.saucedemo.com");
        driver.findElement(By.id("user-name")).sendKeys(LOCKEDUSERNAME);
        driver.findElement(By.id("password")).sendKeys(PASSWORD);
        driver.findElement(By.id("login-button")).click();

        driver.findElement(By.id("user-name")).sendKeys(Keys.chord(Keys.CONTROL + "a"), Keys.BACK_SPACE);
        driver.findElement(By.id("password")).sendKeys(Keys.chord(Keys.CONTROL + "a"), Keys.BACK_SPACE);

        //assert the error
        String expected = "Epic sadface: Sorry, this user has been locked out.";
        assertEquals(expected, driver.findElement(By.className("error-message-container")).getText());

        //attempt to get in with the normal user
        logIn(USERNAME, PASSWORD);
    }

    @Test
    public void Glitched_User_Experience(){
        setUp("https://www.saucedemo.com");
        logIn(GLITCHUSERNAME, PASSWORD);

        //jump in with the Glitched user 
        driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
        driver.findElement(By.id("shopping_cart_container")).click();

        WebElement cartPageElement = driver.findElement(By.className("cart_list"));
        wait.until(d -> cartPageElement.isDisplayed());

	    String cartItemName = driver.findElement(By.className("inventory_item_name")).getText();
	    assertEquals(cartItemName, "Sauce Labs Backpack");

	    driver.findElement(By.id("checkout")).click();
	    WebElement checkoutPageElement = driver.findElement(By.id("checkout_info_container"));
	    wait.until(d -> checkoutPageElement.isDisplayed());

        driver.findElement(By.id("first-name")).sendKeys("John");
        driver.findElement(By.id("last-name")).sendKeys("Doe");
        driver.findElement(By.id("postal-code")).sendKeys("10001");
        driver.findElement(By.id("continue")).click();

        String checkoutItemName = driver.findElement(By.className("inventory_item_name")).getText();
        assertEquals(checkoutItemName, "Sauce Labs Backpack");

        driver.findElement(By.id("finish")).click();

        boolean successIsDisplayed = driver.findElement(By.id("checkout_complete_container")).isDisplayed();
        assertTrue(successIsDisplayed);
    }


}

